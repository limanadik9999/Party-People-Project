$(document).on('submit', '#create_event', function(e){
  e.preventDefault();
  var event_title = $('#event_title').val();
  var event_text = $('#event_text').val();
  var event_image = $('#event_image').val();

  if (event_text != ''){
    $('#event_title').val('');
    $('#event_text').val('');
    $('#event_image').val('');
     $.ajax({
      type:'POST',
      url:"/account/",
      data:{
        event_title:event_title,
        event_text:event_text,
        event_image:event_image,
        csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
      },
      success:function () {
        alert('Successfully created!');
      }
    });
  };
});
