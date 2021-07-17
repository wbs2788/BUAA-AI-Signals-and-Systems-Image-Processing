clear;
clc;
close all;
format compact;
format long;

RGBImg = imread('./imgs/test3.jpg'); %读取图片
grayImg = rgb2gray(RGBImg);
cb_scale = 2;
cr_scale = 1;

[cb_mean, cr_mean, cb_std, cr_std] = cbcrPlate(cb_scale, cr_scale) % 获取数据信息

result = FaceBinarization(RGBImg, cb_mean, cr_mean, cb_std, cr_std, cb_scale, cr_scale); % 图像二值化

result = imfill(result,'holes'); % 填补背景

result = bwareaopen(result, 500); % 去除孤立区

result = imerode(result, ones(5)); % 图像腐蚀操作（为边缘检测服务）

edgeImg = edge(grayImg, 'roberts', 0.1); % Robert边缘检测
edgeImg = ~edgeImg;

result = 255*(double(result) & double(edgeImg)); % 整合获得结果

% 再次进行边缘检测处理，根据宽高比去除不可能是脸部的区域
result = imerode(result, ones(5)); 

result = bwfill(result, 'holes');

result = bwareaopen(result, 500);

[segments, num_segments] = bwlabel(result);
status = regionprops(segments, 'BoundingBox');

width_all = []; height_all = [];
for i=1:num_segments
    width_all = [width_all; status(i).BoundingBox(3)];
    height_all = [height_all; status(i).BoundingBox(4)];
end
 figure;
 subplot(221), hist(width_all, 50), title('标记区域宽的分布图');
 subplot(222), hist(height_all, 50), title('标记区域高的分布图');
 subplot(223), hist(height_all./width_all, 50), title('标记区域高宽比的分布图');

% 展示标记信息
figure, imshow(RGBImg);
for i=1:num_segments
    width = status(i).BoundingBox(3);
    height = status(i).BoundingBox(4);
    ratio = height/width;
    if ratio > 3 || ratio < 0.75 || (width < 40 & height < 50) continue; end
    rectangle('position', status(i).BoundingBox, 'edgecolor', 'r');
end 