import os
import torch
from torchvision import *
from torch.profiler import *

epochs = 20
batch_size = 1

# model = models.alexnet()
# model = models.squeezenet1_0()
# model = models.vgg11()
model = models.shufflenet_v2_x0_5()
# model = models.mobilenet_v2()
# model = models.resnet18()
# model = models.resnet50()

starter, ender = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
times = torch.zeros(epochs)

test_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5],
                         std=[0.5, 0.5, 0.5])
])

cpu_num_list = [1, 1, 2, 4, 8, 16, 32, 64]
for cpu_num in cpu_num_list:
    # cpu_num = cpu_count()  # 获取最大核心数目
    os.environ['OMP_NUM_THREADS'] = str(cpu_num)
    os.environ['OPENBLAS_NUM_THREADS'] = str(cpu_num)
    os.environ['MKL_NUM_THREADS'] = str(cpu_num)
    os.environ['VECLIB_MAXIMUM_THREADS'] = str(cpu_num)
    os.environ['NUMEXPR_NUM_THREADS'] = str(cpu_num)
    torch.set_num_threads(cpu_num)

    for epoch in range(epochs):
        starter.record()

        device = torch.device("cuda:0")
        model.to(device)

        input_data = datasets.ImageFolder(root='/data/imagenet/val',
                                          transform=test_transform)
        dataloader = torch.utils.data.DataLoader(dataset=input_data,
                                                 batch_size=batch_size,
                                                 shuffle=True,
                                                 num_workers=4)


        # 时间接口
        # starter, ender = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
        # times = torch.zeros(len(dataloader))  # 存储每轮iteration的时间

        # # GPU预热
        # with torch.no_grad():
        #     for _ in range(100):
        #         _ = model(input_data)
        # torch.cuda.synchronize()

        # 推理
        with torch.no_grad():
            for i, (img, label) in enumerate(dataloader):
                # starter.record()
                img = img.to(device)
                _ = model(img)
                # ender.record()
                # 同步GPU
                torch.cuda.synchronize()
                # curr_time = starter.elapsed_time(ender)  # 计算时间
                # times[i] = curr_time
                # print(curr_time)
        ender.record()
        curr_time = starter.elapsed_time(ender)  # 计算时间
        times[epoch] = curr_time

    mean_time = times.mean().item()
    # print("CPU_num: {}, Inference time: {:.6f}, FPS: {} ".format(cpu_num, mean_time, 1000 / mean_time))
    print("{:.6f}".format(mean_time))
