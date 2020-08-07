
// Backup
// <script type="text/javascript">
//                         // var num_of_likes = parseInt('{{post.likes.all.count}}'),like_id = ''.concat('#', '{{post.id}}'),
//                         //     post_id = '{{post.id}}', initial_value = parseInt('{{post.likes.all.count}}'), 

//                         // ;

//                         $(document).ready(function(){

//                             let num_of_likes =  parseInt('{{post.likes.all.count}}'),
//                             like_id = ''.concat('#', '{{post.id}}');
//                             $(like_id).on('click',function(event){

//                         let post_id = '{{post.id}}' 
//                         $.ajax({
//                             type: "POST",
//                             url: "{% url 'accounts:likes-api-post' post.id %}",
//                             data: {"post_id": post_id, 'csrfmiddlewaretoken': '{{ csrf_token}}' },
//                             dataType: 'json',
//                             success: function(data){
//                                 let like_button =  $(like_id),
//                                 initial_value = parseInt('{{post.likes.all.count}}');

//                                 status_of_button = $(like_id).attr('name');
//                                 if (data.status == true && num_of_likes === initial_value && status_of_button == 'like-button-not-liked'){  
//                                     like_button.css('color','#0275d8')
//                                     num_of_likes += 1;
//                                     document.getElementById(''.concat('span', '{{post.id}}')).textContent=(num_of_likes);

//                                 }else if (data.status == false && num_of_likes === (initial_value + 1) && status_of_button === 'like-button-not-liked'){
//                                     like_button.css('color','grey')
//                                     num_of_likes -= 1;
//                                     document.getElementById(''.concat('span', '{{post.id}}')).textContent=(num_of_likes);
                                    
//                                 } else if (data.status == false && num_of_likes === initial_value && status_of_button == 'like-button-liked'){
//                                     like_button.css('color','grey')
//                                     num_of_likes -= 1;
//                                     document.getElementById(''.concat('span', '{{post.id}}')).textContent=(num_of_likes);
//                                 } else if (data.status == true && num_of_likes === (initial_value - 1) && status_of_button == 'like-button-liked'){
//                                     like_button.css('color','#0275d8')
//                                     num_of_likes += 1;
//                                     document.getElementById(''.concat('span', '{{post.id}}')).textContent=(num_of_likes);
//                                 }           
//                             }
//                         });
//                         event.stopImmediatePropagation();
//                         return false;
//                     })
//                     })

//                     </script>