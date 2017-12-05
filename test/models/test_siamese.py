from unittest import TestCase


class TestInception(TestCase):
    def test_forward(self):
        import torch
        from torch.autograd import Variable
        from reid.models.inception import InceptionNet

        # model = Inception(num_classes=5, num_features=256, dropout=0.5)
        # x = Variable(torch.randn(10, 3, 144, 56), requires_grad=False)
        # y = model(x)
        # self.assertEquals(y.size(), (10, 5))

        model = InceptionNet(num_features=8, norm=True, dropout=0)
        x = Variable(torch.randn(10, 3, 144, 56), requires_grad=False)
        y = model(x)
        self.assertEquals(y.size(), (10, 8))
        self.assertEquals(y.norm(2, 1).max(), 1)
        self.assertEquals(y.norm(2, 1).min(), 1)


if __name__ == '__main__':
    import torch
    from torch.autograd import Variable
    from reid.models import Siamese

    model = Siamese()
    x1 = Variable(torch.randn(4, 2048, 8, 4), requires_grad=False)
    x2 = Variable(torch.randn(4, 2048, 8, 4), requires_grad=False)

    y = model(x1, x2)

    print(y.size())
