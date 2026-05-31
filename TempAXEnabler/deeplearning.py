# %%
# 패키지 import
import os
import glob
import math
import os.path as osp
import random
import numpy as np
import pandas as pd
import json
import time
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision
from torchvision import models, transforms
from torch.utils.data import random_split, WeightedRandomSampler
from torch.optim import lr_scheduler

# %%
# 난수 시드 설정
torch.manual_seed(1234)
np.random.seed(1234)
random.seed(1234)

# network 모델 설정
# 0: vgg16
# 1: resnet50
# 2: resnet18
# 3: Mobilenet V2
# 4: EfficientNet-B0

model_names = {
    0: "VGG16",
    1: "ResNet50",
    2: "ResNet18",
    3: "MobileNet V2",
    4: "MobileNet V3 Large",
    5: "EfficientNet-B0"
}
model_batch_sizes = {
    0: 16,  # VGG16: 파라미터가 매우 많아 16이 안전합니다.
    1: 32,  # ResNet50: 32가 가장 무난합니다.
    2: 64,  # ResNet18: 가벼워서 64\~128 가능 (안전하게 64)
    3: 64,  # MobileNet V2: 매우 가벼움 (안전하게 64, 여유 있으면 128)
    4: 64,  # MobileNet V3 Large: 매우 가벼움 (안전하게 64, 여유 있으면 128)
    5: 32  # EfficientNet-B0: 파라미터는 적지만 메모리 점유율이 있어 32 추천
}

network = 1  # 분류 모델 선택
num_classes = 2  # 분류 개수
use_mini_run = False  # 미니 데이터셋 런
eta_min_value = 0.0001  # 학습률 최솟값
num_epochs = 30  # 학습 Epoch


# %%
# 입력 화상의 전처리 클래스
# 훈련 시와 추론 시 처리가 다르다.

class ImageTransform():
    """
    화상 전처리 클래스.
    훈련 시에는 RandomResizedCrop, RandomHorizontalFlip, RandomRotation으로 데이터를 확장한다.
    """

    def __init__(self, resize, mean, std):
        self.data_transform = {
            'train': transforms.Compose([
                transforms.RandomResizedCrop(resize, scale=(0.7, 1.0)),  # 크기 변경 및 자르기 (Crop)
                transforms.RandomHorizontalFlip(),  # 좌우 반전 (Flip)
                transforms.RandomRotation(degrees=60),  # [추가] -15\~15도 랜덤 회전 (Rotate)
                transforms.ToTensor(),  # 텐서 변환
                transforms.Normalize(mean, std)  # 표준화
            ]),
            'val': transforms.Compose([
                transforms.Resize(resize),
                transforms.CenterCrop(resize),
                transforms.ToTensor(),
                transforms.Normalize(mean, std)
            ])
        }

    def __call__(self, img, phase='train'):
        """
        Parameters
        ----------
        phase : 'train' or 'val'
            전처리 모드 지정
        """
        return self.data_transform[phase](img)


# %%
# 훈련 시 화상 전처리 동작 확인
# 실행할 때마다 처리 결과 화상이 바뀐다.

# 3. 화상 전처리, 처리된 화상 표시
size = 224
mean = (0.485, 0.456, 0.406)
std = (0.229, 0.224, 0.225)


# %%
# 데이터 파일 경로를 저장하는 리스트 변수 생성
def make_datapath_list(root_path):
    """
    지정된 루트 디렉토리 하위의 모든 이미지 파일을 찾아 경로 리스트를 반환합니다.

    Parameters
    ----------
    root_path : str
        데이터가 위치한 루트 디렉토리 경로

    Returns
    -------
    path_list : list
        이미지 파일의 절대 경로가 담긴 리스트
    """

    # 이미지 파일 확장자 정의 (필요에 따라 추가 가능)
    img_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff')

    path_list = []

    # os.walk를 사용하여 하위 디렉토리까지 재귀적으로 탐색
    for root, dirs, files in os.walk(root_path):
        for file in files:
            # 파일 확장자가 이미지인지 확인 (대소문자 무시)
            if file.lower().endswith(img_extensions):
                # 경로 결합
                full_path = os.path.join(root, file)
                path_list.append(full_path)

    return path_list


# 실행
root_dir = r"D:\SourceCode\AXEnabler\EL_WELDER\Images"

full_list = make_datapath_list(root_path=root_dir)

# 미니 학습 임시용
if (use_mini_run):
    full_list = random.sample(full_list, int(len(full_list) * 0.05))

print("총 이미지 개수", len(full_list))


# %%
class WeldingDataset(data.Dataset):
    """
    용접(Welding) 화상 데이터셋 클래스.
    PyTorch의 Dataset 클래스를 상속받아 구현.

    Attributes
    ----------
    file_list : 리스트
        이미지 파일 경로가 저장된 리스트
    transform : object
        전처리 클래스의 인스턴스 (ImageTransform)
    phase : 'train' or 'val'
        학습 모드인지 검증 모드인지 설정
    """

    def __init__(self, file_list, transform=None, phase='train'):
        self.file_list = file_list  # 파일 경로 리스트
        self.transform = transform  # 전처리 인스턴스
        self.phase = phase  # train 또는 val

    def __len__(self):
        '''전체 이미지 개수를 반환'''
        return len(self.file_list)

    def __getitem__(self, index):
        '''
        index번째 이미지와 라벨을 가져와서 전처리 후 반환
        '''

        # 1. 이미지 로드
        img_path = self.file_list[index]
        # RGB로 변환 (흑백 이미지 등이 섞여 있을 경우 에러 방지)
        img = Image.open(img_path).convert('RGB')

        # 2. 이미지 전처리 (Augmentation 등)
        img_transformed = self.transform(img, self.phase)

        # 3. 라벨 추출 (파일 경로에 'NG'가 포함되어 있으면 1, 아니면 0)
        # 예: "./data/train/NG/image_01.jpg" -> NG 포함됨 -> 1
        if 'NG' in img_path:
            label = 1
        elif 'OK' in img_path:
            label = 0
        else:
            # 파일명 규칙이 다를 경우를 대비한 예외 처리 (필요 시 수정)
            label = -1

        return img_transformed, label, img_path


# 개수 계산 (90% : 10%)
val_ratio = 0.1
val_size = int(val_ratio * len(full_list))
train_size = len(full_list) - val_size

# 랜덤 분할
train_list, val_list = random_split(full_list, [train_size, val_size])

train_dataset = WeldingDataset(file_list=train_list, transform=ImageTransform(size, mean, std), phase='train')
val_dataset = WeldingDataset(file_list=val_list, transform=ImageTransform(size, mean, std), phase='val')
# %%
# 1. 클래스별 개수 확인 (train_dataset.file_list 기준)
# NG(1), OK(0) 개수 세기
ng_count = 0
ok_count = 0

for path in train_dataset.file_list:
    if 'NG' in path:
        ng_count += 1
    else:
        ok_count += 1

print(f"OK 개수: {ok_count}, NG 개수: {ng_count}")

# 2. 클래스별 가중치 계산 (개수의 역수)
# 개수가 적을수록 가중치가 커집니다. (이렇게 하면 50:50 비율로 학습하게 됩니다)
weight_for_ng = math.sqrt(1.0 / ng_count)
weight_for_ok = math.sqrt(1.0 / ok_count)
print("Sampling OK Weight : ", weight_for_ok, "Sampling NG Weight : ", weight_for_ng)
# 3. 모든 샘플에 가중치 부여 (samples_weights 리스트 생성)
samples_weights = []
for path in train_dataset.file_list:
    if 'NG' in path:
        samples_weights.append(weight_for_ng)
    else:
        samples_weights.append(weight_for_ok)

# 텐서로 변환
samples_weights = torch.DoubleTensor(samples_weights)

# 4. Sampler 생성
# replacement=True: 한 번 뽑힌 데이터도 다시 뽑힐 수 있음 (그래야 적은 데이터를 많이 뽑을 수 있음)
sampler = WeightedRandomSampler(
    weights=samples_weights,
    num_samples=len(samples_weights),
    replacement=True
)
# %%
# 미니 배치 크기 지정
batch_size = model_batch_sizes[network]

# 데이터 로더 작성
train_dataloader = torch.utils.data.DataLoader(
    train_dataset,
    batch_size=batch_size,
    sampler=sampler,
    shuffle=False)

val_dataloader = torch.utils.data.DataLoader(
    val_dataset,
    batch_size=batch_size,
    shuffle=False)

# 사전형 변수에 정리
dataloaders_dict = {"train": train_dataloader, "val": val_dataloader}

# 동작 확인
batch_iterator = iter(dataloaders_dict["train"])  # 반복자(iterator)로 변환
inputs, labels, path = next(batch_iterator)  # 첫 번째 요소 추출
print(inputs.size())
print(labels)

# %%
# 모델 불러오기 및 설정
if network == 0:  # VGG16
    # weights='DEFAULT'는 최신 PyTorch 권장 방식 (기존 pretrained=True와 동일)
    net = models.vgg16(weights=models.VGG16_Weights.DEFAULT)

    # 1. 모든 파라미터 고정 (Freeze)
    for param in net.parameters():
        param.requires_grad = False

    # 2. 마지막 층 교체 (교체된 층은 자동으로 requires_grad=True가 됨)
    in_features = net.classifier[6].in_features
    net.classifier[6] = nn.Linear(in_features, num_classes)

elif network == 1:  # ResNet50
    net = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)

    for param in net.parameters():
        param.requires_grad = False

    in_features = net.fc.in_features
    net.fc = nn.Linear(in_features, num_classes)

elif network == 2:  # ResNet18 (추천)
    net = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

    for param in net.parameters():
        param.requires_grad = False

    in_features = net.fc.in_features
    net.fc = nn.Linear(in_features, num_classes)

elif network == 3:  # MobileNet V2
    net = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.DEFAULT)

    for param in net.parameters():
        param.requires_grad = False

    # MobileNet V2의 classifier는 [Dropout, Linear] 구조임. [1]이 Linear
    in_features = net.classifier[1].in_features
    net.classifier[1] = nn.Linear(in_features, num_classes)

elif network == 4:  # MobileNet V3
    net = models.mobilenet_v3_large(weights='DEFAULT')

    for param in net.parameters():
        param.requires_grad = False

    # MobileNet V3 Large의 classifier 구조:
    # (0): Linear, (1): Hardswish, (2): Dropout, (3): Linear (출력층)
    in_features = net.classifier[3].in_features
    net.classifier[3] = nn.Linear(in_features, num_classes)

elif network == 5:  # EfficientNet-B0
    net = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)

    for param in net.parameters():
        param.requires_grad = False

    # EfficientNet의 classifier도 [Dropout, Linear] 구조. [1]이 Linear
    in_features = net.classifier[1].in_features
    net.classifier[1] = nn.Linear(in_features, num_classes)

# 훈련 모드로 설정
net.train()

print(f"네트워크 설정 완료: 학습된 가중치를 읽어들여 훈련 모드로 설정했습니다. [현재 모델: {model_names[network]}]")

# %%
# 손실 함수 설정
# 1. 학습 데이터에서 OK와 NG 개수 세기
# (train_list는 앞서 만든 파일 경로 리스트라고 가정)
num_ng = sum(1 for path in full_list if 'NG' in path)
num_ok = len(full_list) - num_ng

print(f"OK 개수: {num_ok}, NG 개수: {num_ng}")

# 2. 가중치 계산
# NG가 0개일 경우를 대비해 1e-5 같은 작은 수를 더하거나 예외처리 필요
# 50배 정도 OK 이미지가 많아서 가중치 5배 둠
if num_ng > 0:
    weight_value = math.log(num_ok / num_ng)

else:
    weight_value = 1.0  # NG가 없으면 가중치 1 (기본값)

print(f"적용할 가중치(pos_weight): {weight_value:.2f}")

# 3. 텐서로 변환 및 디바이스 할당 (GPU 사용 시 필수)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
pos_weight = torch.tensor([weight_value]).to(device)

# 4. 손실 함수 정의 (BCEWithLogitsLoss 사용 권장)
# BCEWithLogitsLoss는 내부적으로 Sigmoid를 포함하므로,
# 모델의 마지막 레이어에 Sigmoid를 따로 붙이지 않아야 합니다.
# criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
weights = torch.tensor([1.0, weight_value]).to(device)  # [OK가중치, NG가중치]
# criterion = nn.CrossEntropyLoss(weight=weights)
criterion = nn.CrossEntropyLoss()

# %%
# 전이학습에서 학습시킬 파라미터를 params_to_update 변수에 저장
params_to_update = []

print(f"Selected Network: {network}")
print("Params to learn:")

for name, param in net.named_parameters():
    if param.requires_grad == True:
        params_to_update.append(param)
        print(f"\t{name}")

# params_to_update의 내용 확인
print("--------------")
print(params_to_update)

# %%
# 최적화 기법 설정
# 1. 초기 학습률 0.001 설정
optimizer = optim.Adam(params=params_to_update, lr=0.001)


# 2. 스케줄러 설정: milestones 리스트에 있는 에폭에서만 gamma를 곱함
# milestones=[10]: 10번째 에폭이 끝날 때 딱 한 번만 작동
# gamma=0.1: 현재 학습률에 0.1을 곱함

# %%
# 모델을 학습시키는 함수 작성
def train_model(net, dataloaders_dict, criterion, optimizer, num_epochs):
    # 1. GPU/CPU 장치 설정
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"사용 장치: {device}")
    print(f"Epoch : {num_epochs}, Batch Size: {batch_size}")
    net.to(device)  # 모델을 GPU로 이동
    val_size = 5
    inference_result = {'Phase': [],
                        'Epoch': [],
                        'Time': [],
                        'Loss': [],
                        'Acc': [],
                        'lr': []
                        }
    for epoch in range(num_epochs):

        # 2. val_size마다 검증(val) 수행, 그 외에는 학습(train)만 수행
        if (epoch + 1) % val_size == 0:
            phases = ['train', 'val']
            print(f'Epoch {epoch + 1}/{num_epochs} (검증 및 저장 수행)')
        else:
            phases = ['train']
            print(f'Epoch {epoch + 1}/{num_epochs}')

        print('-------------')

        for phase in phases:
            start_time = time.time()
            if phase == 'train':
                net.train()
            else:
                net.eval()

            epoch_loss = 0.0
            epoch_corrects = 0

            # 데이터 로더 루프
            for inputs, labels, paths in tqdm(dataloaders_dict[phase]):
                # 3. 데이터를 GPU로 이동
                inputs = inputs.to(device)
                labels = labels.to(device)

                # (주의) BCE Loss 사용 시 아래 주석 해제 필요
                # labels = labels.unsqueeze(1).float()

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = net(inputs)
                    loss = criterion(outputs, labels)

                    # (주의) 예측 방식: CrossEntropy면 torch.max, BCE면 (outputs >= 0).float()
                    _, preds = torch.max(outputs, 1)
                    # preds = (outputs >= 0.0).float() # BCE 사용 시 이걸로 교체

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                    epoch_loss += loss.item() * inputs.size(0)
                    epoch_corrects += torch.sum(preds == labels.data)

            # 4. [중요] 들여쓰기 수정: 에포크가 끝난 후 평균 계산
            epoch_loss = epoch_loss / len(dataloaders_dict[phase].dataset)
            epoch_acc = epoch_corrects.double() / len(dataloaders_dict[phase].dataset)

            inference_result['Phase'].append(phase)
            inference_result['Epoch'].append(epoch + 1)
            inference_result['Time'].append(time.time() - start_time)
            inference_result['Loss'].append(epoch_loss)
            inference_result['Acc'].append(epoch_acc.item())
            inference_result['lr'].append(scheduler.get_last_lr()[0])

            print('{} Loss : {:.8f}, Acc : {:.8f}, lr : {:.8f}'.format(
                phase, epoch_loss, epoch_acc, scheduler.get_last_lr()[0]))
            print()
            # 5. epoch마다 스케줄러 업데이트
        scheduler.step()

        # 6. val_size마다 모델 저장
        if (epoch + 1) % val_size == 0 and (epoch + 1) != num_epochs:
            save_path = f'Model\\model_{model_names[network]}_weights_epoch_{epoch + 1}.pth'
            # 저장 폴더가 없다면 만드는 로직 추가 가능
            torch.save(net.state_dict(), save_path)
            print(f"-> 모델 저장 완료: {save_path}")

    # 학습을 종료할 때는 가중치를 저장해야 한다.
    save_path = f'Model\\model_{model_names[network]}_weights_epoch_{epoch + 1}.pth'
    # 저장 폴더가 없다면 만드는 로직 추가 가능
    torch.save(net.state_dict(), save_path)
    print(f"-> 모델 저장 완료: {save_path}")

    df_result = pd.DataFrame(inference_result)
    df_result.to_csv(f'Inference\\{model_names[network]}_train.csv', index=False, encoding='utf-8-sig')


# %%

# T_max: 학습률이 최소값에 도달하는 주기 (보통 총 에폭 수와 같게 설정)
# eta_min: 학습률 하한선 (0.00001 밑으로는 절대 안 떨어짐)
scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs, eta_min=eta_min_value)

# 학습 Run
train_model(net, dataloaders_dict, criterion, optimizer, num_epochs)
# %%
# 결과를 담을 빈 리스트 생성
all_preds = []
all_labels = []
all_filenames = []

net.eval()  # 평가 모드
eval_mode = "val"

with torch.no_grad():
    # Dataset을 수정했으므로 변수를 3개로 받습니다 (inputs, labels, paths)
    for inputs, labels, paths in dataloaders_dict[eval_mode]:
        inputs = inputs.to(device)
        labels = labels.to(device)

        outputs = net(inputs)
        _, preds = torch.max(outputs, 1)

        # 결과 저장
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_filenames.extend(paths)  # 파일 경로(이름) 저장

# Pandas DataFrame 생성
df_result = pd.DataFrame({
    'filename': all_filenames,
    'target': all_labels,
    'prediction': all_preds
})

# 정답 여부 컬럼 추가 (선택 사항)
df_result['correct'] = df_result['target'] == df_result['prediction']

# CSV 파일로 저장 (한글 깨짐 방지를 위해 utf-8-sig 권장)
df_result.to_csv(f'Result\\{model_names[network]}_inference_{eval_mode}.csv', index=False, encoding='utf-8-sig')

print("CSV 저장 완료!")
display(df_result.head())
# %%
# 리스트를 Pandas Series로 변환 (이름을 붙여주면 표에 라벨로 나옵니다)
y_true = pd.Series(all_labels, name='actual')
y_pred = pd.Series(all_preds, name='Predicted')

# 교차표 생성 (sklearn 없이 가능)
df_cm = pd.crosstab(y_true, y_pred)

# Jupyter Notebook에서 출력
display(df_cm)
# %%
# 결과를 담을 빈 리스트 생성
all_preds = []
all_labels = []
all_filenames = []

net.eval()  # 평가 모드
eval_mode = "train"

with torch.no_grad():
    # Dataset을 수정했으므로 변수를 3개로 받습니다 (inputs, labels, paths)
    for inputs, labels, paths in dataloaders_dict[eval_mode]:
        inputs = inputs.to(device)
        labels = labels.to(device)

        outputs = net(inputs)
        _, preds = torch.max(outputs, 1)

        # 결과 저장
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_filenames.extend(paths)  # 파일 경로(이름) 저장

# Pandas DataFrame 생성
df_result = pd.DataFrame({
    'filename': all_filenames,
    'target': all_labels,
    'prediction': all_preds
})

# 정답 여부 컬럼 추가 (선택 사항)
df_result['correct'] = df_result['target'] == df_result['prediction']

# CSV 파일로 저장 (한글 깨짐 방지를 위해 utf-8-sig 권장)
df_result.to_csv(f'Result\\{model_names[network]}_inference_{eval_mode}.csv', index=False, encoding='utf-8-sig')

print("CSV 저장 완료!")
display(df_result.head())