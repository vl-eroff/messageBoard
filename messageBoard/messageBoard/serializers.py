from django.core.serializers import serialize

class UserSerializer:

  def serialize(self, user):

    data = serialize('json', [user, ])
    return data.strip('[]')  # Remove brackets for single object

class TradeSerializer:

  def serialize(self, trade):

    data = serialize('json', [trade, ])
    return data.strip('[]')

class ImageSerializer:

  def serialize(self, image):

    data = serialize('json', [image, ])
    return data.strip('[]')