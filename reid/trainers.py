from __future__ import print_function, absolute_import
import time, collections

import torch
from torch.autograd import Variable
import torchvision.utils as vutils
from .evaluation_metrics import accuracy
from .loss import OIMLoss, TripletLoss, TupletLoss
from .utils.meters import AverageMeter
from lz import *
from tensorboardX import SummaryWriter
from reid.utils import to_numpy, to_torch


class BaseTrainer(object):
    def __init__(self, model, criterion, dbg=False, logs_at='work/vis'):
        super(BaseTrainer, self).__init__()
        self.model = model
        self.criterion = criterion
        self.dbg = dbg
        if dbg:
            mkdir_p(logs_at, delete=True)
            self.writer = SummaryWriter(logs_at)
            self.iter = 0

    def train(self, epoch, data_loader, optimizer, print_freq=1):
        self.model.train()

        batch_time = AverageMeter()
        data_time = AverageMeter()
        losses = AverageMeter()
        precisions = AverageMeter()

        end = time.time()
        for i, inputs in enumerate(data_loader):
            data_time.update(time.time() - end)

            inputs, targets = self._parse_data(inputs)
            loss, prec1 = self._forward(inputs, targets)
            if isinstance(targets, tuple):
                targets, _ = targets
            losses.update(loss.data[0], targets.size(0))
            precisions.update(prec1, targets.size(0))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_time.update(time.time() - end)
            end = time.time()

            if (i + 1) % print_freq == 0:
                print('Epoch: [{}][{}/{}]\t'
                      'Time {:.3f} ({:.3f})\t'
                      'Data {:.3f} ({:.3f})\t'
                      'Loss {:.3f} ({:.3f})\t'
                      'Prec {:.2%} ({:.2%})\t'
                      .format(epoch, i + 1, len(data_loader),
                              batch_time.val, batch_time.avg,
                              data_time.val, data_time.avg,
                              losses.val, losses.avg,
                              precisions.val, precisions.avg))
        return collections.OrderedDict({
            'ttl-time': batch_time.avg,
            'data-time': data_time.avg,
            'loss': losses.avg,
            'prec': precisions.avg
        })

    def _parse_data(self, inputs):
        raise NotImplementedError

    def _forward(self, inputs, targets):
        raise NotImplementedError


class VerfTrainer(BaseTrainer):
    def _parse_data(self, inputs):
        imgs, fnames, pids, _ = inputs
        inputs = [Variable(imgs.cuda(), requires_grad=False)]
        info = None

        # info = pd.DataFrame.from_dict({
        #     'fnames': fnames,
        #     'pids': pids.cpu().numpy(),
        #     'inds': range(len(fnames))
        # })
        # info = pd.concat([info, info], axis=0)
        # info.reset_index(drop=True, inplace=True)

        targets = Variable(pids.cuda(), requires_grad=False)
        return inputs, (targets, info)

    def _forward(self, inputs, targets):
        targets, info = targets
        # self.model.eval()
        if self.freeze == 'embed':
            # self.model.module.base_model.eval()
            self.model.module.embed_model.eval()
        pred, y, info = self.model(inputs[0], targets, info)
        if info is not None:
            write_df(info, 'dbg.hard.h5')
            print(
                np.array(((pred.data[:, 1] > pred.data[:, 0]).type_as(y.data) == y.data).cpu().numpy()).mean()
            )
            exit(0)
        loss = self.criterion(pred, y)
        prec1, = accuracy(pred.data, y.data)
        # ((pred.data[:,1] > pred.data[:,0]).type_as(y.data) == y.data).cpu().numpy()
        return loss, prec1[0]


def stat(tensor):
    return tensor.min(), tensor.mean(), tensor.max(), tensor.std(), tensor.size()


class SiameseTrainer(BaseTrainer):
    def _parse_data(self, inputs):
        (imgs1, _, pids1, _), (imgs2, _, pids2, _) = inputs
        inputs = [Variable(imgs1), Variable(imgs2)]
        targets = Variable((pids1 == pids2).long().cuda())
        return inputs, targets

    def _forward(self, inputs, targets):
        outputs = self.model(*inputs)
        loss = self.criterion(outputs, targets)
        prec1, = accuracy(outputs.data, targets.data)
        return loss, prec1[0]


def stat_(writer, tag, tensor, iter):
    writer.add_scalars('groups/' + tag, {
        'mean': torch.mean(tensor),
        'media': torch.median(tensor),
        'min': torch.min(tensor),
        'max': torch.max(tensor)
    }, iter)


class Trainer(BaseTrainer):
    def _parse_data(self, inputs):
        imgs, fnames, pids, _ = inputs
        inputs = [Variable(imgs.cuda(), requires_grad=False)]
        targets = Variable(pids.cuda(), requires_grad=False)
        return inputs, targets, fnames

    def _forward(self, inputs, targets):
        outputs = self.model(*inputs)
        if self.dbg and self.iter % 1000 == 0:
            self.writer.add_histogram('1_input', inputs[0], self.iter)
            self.writer.add_histogram('2_feature', outputs, self.iter)
            x = vutils.make_grid(to_torch(inputs[0]), normalize=True, scale_each=True)
            self.writer.add_image('input', x, self.iter)

        if isinstance(self.criterion, torch.nn.CrossEntropyLoss):
            loss = self.criterion(outputs, targets)
            prec, = accuracy(outputs.data, targets.data)
            prec = prec[0]
        elif isinstance(self.criterion, OIMLoss):
            loss, outputs = self.criterion(outputs, targets)
            prec, = accuracy(outputs.data, targets.data)
            prec = prec[0]
        elif isinstance(self.criterion, TripletLoss):
            if self.dbg and self.iter % 10 == 0:
                loss, prec, replay_ind, dist, dist_ap, dist_an = self.criterion(outputs, targets, dbg=self.dbg)
                diff = dist_an - dist_ap
                self.writer.add_histogram('an-ap', diff, self.iter)
                # self.writer.add_histogram('an-ap/auto', diff, self.iter, 'auto')

                stat_(self.writer, 'an-ap', diff, self.iter)
                self.writer.add_scalar('vis/loss', loss, self.iter)
                self.writer.add_scalar('vis/prec', prec, self.iter)
                self.writer.add_histogram('dist', dist, self.iter)
                self.writer.add_histogram('ap', dist_ap, self.iter)
                self.writer.add_histogram('an', dist_an, self.iter)
            else:
                loss, prec, replay_ind = self.criterion(outputs, targets, dbg=False)

        elif isinstance(self.criterion, TupletLoss):
            loss, prec = self.criterion(outputs, targets)
        else:
            raise ValueError("Unsupported loss:", self.criterion)
        self.iter += 1
        return loss, prec, replay_ind

    def train(self, epoch, data_loader, optimizer, print_freq=1):
        self.model.train()

        batch_time = AverageMeter()
        data_time = AverageMeter()
        losses = AverageMeter()
        precisions = AverageMeter()

        end = time.time()
        for i, inputs in enumerate(data_loader):
            data_time.update(time.time() - end)
            inputs, targets, fnames = self._parse_data(inputs)
            global_inds = [data_loader.fname2ind[fn] for fn in fnames]
            loss, prec1, replay_ind = self._forward(inputs, targets)
            if isinstance(targets, tuple):
                targets, _ = targets
            losses.update(loss.data[0], targets.size(0))
            precisions.update(prec1, targets.size(0))

            sampler = data_loader.sampler
            probs = np.array(sampler.info.probs)
            alpha=0.9
            probs *= alpha
            for ind_, prob_ in zip(global_inds, replay_ind):
                probs[ind_] = probs[ind_] + (1-alpha) * prob_
            sampler.info['probs'] = probs

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            batch_time.update(time.time() - end)
            end = time.time()

            if (i + 1) % print_freq == 0:
                print('Epoch: [{}][{}/{}]\t'
                      'Time {:.3f} ({:.3f})\t'
                      'Data {:.3f} ({:.3f})\t'
                      'Loss {:.3f} ({:.3f})\t'
                      'Prec {:.2%} ({:.2%})\t'
                      .format(epoch, i + 1, len(data_loader),
                              batch_time.val, batch_time.avg,
                              data_time.val, data_time.avg,
                              losses.val, losses.avg,
                              precisions.val, precisions.avg))
        return collections.OrderedDict({
            'ttl-time': batch_time.avg,
            'data-time': data_time.avg,
            'loss': losses.avg,
            'prec': precisions.avg
        })
