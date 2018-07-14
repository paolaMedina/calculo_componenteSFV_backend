from django.forms import FileInput
from django.utils.safestring import mark_safe 
 

class KrajeeFileInputWidget(FileInput):
    """
    See `http://plugins.krajee.com/file-input`
    """
    def render(self, name, value, attrs=None):
        widgets_html = super(FileInput, self).render(name, value, attrs)
        # attrs['id'] is the ID of the entire widget, append the prefix to chose the sub-widget
        myid = attrs['id']
        scriptKrajeeFileInput = self.getScriptKrajeeFileInputString(myid)
        return mark_safe(widgets_html + ' ' + scriptKrajeeFileInput)
    def getScriptKrajeeFileInputString(self, elementId):
        return """
         <script>
         $('#%s').fileinput({
            theme: 'fa',
            language: 'es', 
            uploadUrl: '#',
            allowedFileExtensions: ['csv',], 
            maxFilesNum: 1,  
            showUpload: false, 
            showUploadedThumbs: false,  
            dropZoneEnabled: false,
             
         });
         </script>
        """ % elementId
