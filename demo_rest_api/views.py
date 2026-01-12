from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    def put(self, request, id):
        """Reemplaza completamente los datos de un elemento, excepto el ID"""
        data = request.data
        
        # Buscar el elemento en la lista
        item_index = None
        for index, item in enumerate(data_list):
            if item['id'] == id:
                item_index = index
                break
        
        if item_index is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validar campos requeridos
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Faltan campos requeridos (name, email).'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reemplazar completamente el elemento, manteniendo el ID original
        new_item = {
            'id': id,
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)
        }
        
        data_list[item_index] = new_item
        
        return Response({'message': 'Elemento actualizado exitosamente.', 'data': new_item}, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        """Actualiza parcialmente los campos de un elemento"""
        data = request.data
        
        # Buscar el elemento en la lista
        item_index = None
        for index, item in enumerate(data_list):
            if item['id'] == id:
                item_index = index
                break
        
        if item_index is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar solo los campos proporcionados
        current_item = data_list[item_index]
        
        if 'name' in data:
            current_item['name'] = data['name']
        if 'email' in data:
            current_item['email'] = data['email']
        if 'is_active' in data:
            current_item['is_active'] = data['is_active']
        
        return Response({'message': 'Elemento actualizado parcialmente.', 'data': current_item}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """Elimina lógicamente un elemento marcándolo como inactivo"""
        # Buscar el elemento en la lista
        item_index = None
        for index, item in enumerate(data_list):
            if item['id'] == id:
                item_index = index
                break
        
        if item_index is None:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Eliminación lógica: marcar como inactivo
        data_list[item_index]['is_active'] = False
        
        return Response({'message': 'Elemento eliminado exitosamente.'}, status=status.HTTP_200_OK)