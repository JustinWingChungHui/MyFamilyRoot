from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from common.utils import intTryParse
from gallery.models import Gallery, Image
from gallery_api.serializers import GallerySerializer


class GalleryView(viewsets.GenericViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = GallerySerializer

    def get_queryset(self):
        return Gallery.objects.filter(family_id = self.request.user.family_id).order_by('-last_updated_date')[:20]

    def list(self, request):
        '''
        Lists galleries in users family.
        '''
        queryset = Gallery.objects.filter(family_id = self.request.user.family_id).order_by('-last_updated_date')

        page = self.paginate_queryset(queryset)

        serializer = GallerySerializer(page, many=True)

        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)



    def retrieve(self, request, pk=None):
        '''
        Gets a single Gallery record
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery = get_object_or_404(queryset, pk=pk)
        serializer = GallerySerializer(gallery)
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        '''
        Deletes a gallery record and all its images
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery = get_object_or_404(queryset, pk=pk)

        gallery.delete_all_images()
        gallery.delete()

        return Response('OK')


    def partial_update(self, request, pk=None):
        '''
        Updates title, description and thumbnail of gallery record
        '''
        queryset = Gallery.objects.filter(family_id = request.user.family_id)
        gallery = get_object_or_404(queryset, pk=pk)

        title = request.data.get('title')
        if title:
            gallery.title = title

        description = request.data.get('description')
        if description:
            gallery.description = description

        thumbnail_id = request.data.get("thumbnail_id", None)
        if thumbnail_id is not None:

            thumbnail_id_number, thumbnail_id_number_valid = intTryParse(thumbnail_id)

            if thumbnail_id_number_valid:

                thumbnail_queryset = Image.objects.filter(family_id = request.user.family_id)
                image = get_object_or_404(thumbnail_queryset, pk=thumbnail_id)

                gallery.thumbnail = image.thumbnail
                gallery.thumbnail_height = image.thumbnail_height
                gallery.thumbnail_width = image.thumbnail_width

            else:
                # Remove thumbnail
                gallery.thumbnail = ''
                gallery.thumbnail_height = 0
                gallery.thumbnail_width = 0


        gallery.save()
        serializer = GallerySerializer(gallery)
        return Response(serializer.data)


    def create(self, request):
        '''
        Creates a new gallery
        '''
        family_id = request.user.family_id
        title = request.data.get('title')
        description = request.data.get('description')

        if not title:
            raise ParseError('Must have title')


        gallery = Gallery.objects.create(family_id=family_id, title=title, description=description)
        serializer = GallerySerializer(gallery)

        return Response(serializer.data)

