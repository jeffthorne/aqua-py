from aqua import Aqua

aqua = Aqua(id='administrator', password='password', host='mylo.uw.edu')


aqua.register_image('registryName', 'imageName', 'tag')
image = aqua.get_registered_image('registryName', 'imageName', 'tag')
scan_status = aqua.scan_status('registryName', 'imageName', 'tag')
scan_results = aqua.scan_results('registryName', 'imageName', 'tag')

host_images = aqua.get_registered_images('Host Images')    # retrieve host images
