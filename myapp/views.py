from django.shortcuts import render


import cv2

import matplotlib.pyplot as plt

import numpy as np

import cv2

from skimage.exposure import adjust_sigmoid

from rest_framework.generics import CreateAPIView


from .serializers import ImageSerializer

from rest_framework.response import Response

from rest_framework import serializers, status
import os
import base64

# Opening the image.


class ImageEnhanceApiview(CreateAPIView):

    org_img = None

    serializer_class = ImageSerializer

    # Local path for implementation of local server

    def create(self, request, format=None):
        """
        Takes the request from the post and then processes the algorithm to extract the data and return the result in a
        JSON format
        :param request:
        :param format:
        :return:
        """

        serializer = self.serializer_class(data=request.data)
        print(serializer, "this is data")

        if serializer.is_valid():

            img = self.request.data["image_path"]

            image_path = r"E:/image_enhancement/" + img

            print(image_path, "this is iamge path")

            output = None

            print(self.request.data, "this is requested data")

            if self.request.data["attr"] == "hist":
                print(self.request.data["attr_val"], "this is attr value")

                img = self.hist(int(self.request.data["attr_val"]), image_path)
                is_success, im_buf_arr = cv2.imencode(".jpg", img)
                img = base64.b64encode(im_buf_arr).decode("utf-8")
                # cv2.imwrite(output_path, img)
                output = img
                # print(output)

            elif self.request.data["attr"] == "contrast":
                print(type(self.request.data["attr_val"]), "this is attr value")

                img = self.contrast_Stretch(
                    int(self.request.data["attr_val"]), image_path
                )
                
                is_success, im_buf_arr = cv2.imencode(".jpg", img)
                img = base64.b64encode(im_buf_arr).decode("utf-8")
                # cv2.imwrite(output_path, img)
                output = img

            if self.request.data["attr"] == "gamma":
                print((type(self.request.data["attr_val"]), "this is attr value"))

                img = self.gamma_correction(
                    int(self.request.data["attr_val"]), image_path
                )
                is_success, im_buf_arr = cv2.imencode(".jpg", img)
                img = base64.b64encode(im_buf_arr).decode("utf-8")
                # cv2.imwrite(output_path, img)
                output = img

            # a = cv2.resize(a, (700,700))

            font = cv2.FONT_HERSHEY_SIMPLEX

            return Response(output, status=status.HTTP_200_OK)
        print(type(serializer.data))
        errors = serializer.errors

        response_text = {"status": False, "response": errors}
        return Response(response_text, status=status.HTTP_400_BAD_REQUEST)

    def gamma_correction(self, x, image_path):
        org_img = cv2.imread(image_path)
        print(org_img, "gamma org image")

        if x == 0:

            return org_img
        else:

            invGamma = 1 / x

            table = [((i / 255) ** invGamma) * 255 for i in range(256)]
            table = np.array(table, np.uint8)
            img2 = cv2.LUT(org_img, table)
            return img2

    def hist(self, x, image_path):

        org_img = cv2.imread(image_path)
        if x == 0:
            return org_img
        else:
            gray_image = cv2.cvtColor(org_img, cv2.COLOR_BGR2GRAY)
            print(type(x), "hist x")

            clahe = cv2.createCLAHE(clipLimit=x, tileGridSize=(8, 8))
            img2 = clahe.apply(gray_image)
            print(type(img2))
            return img2

    def contrast_Stretch(
        self, x, image_path,
    ):
        org_img = cv2.imread(image_path)
        # print(org_img, "this is contrast org image")

        if x == 0:

            return org_img
        else:

            # Applying Sigmoid correction.
            img2 = adjust_sigmoid(org_img, gain=x)
            return img2
            # Saving img2.


# cv2.imshow('window', a)
