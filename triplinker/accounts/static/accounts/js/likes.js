
    $(document).ready(function(){

        let num_of_likes =  parseInt(localStorage.getItem("num_of_likes")),
        like_id = '#' + id,
        console.log(like_id)
        csrf_token =  localStorage.getItem("csrf_token");

        $(like_id).on('click',function(event){
        let post_id = localStorage.getItem("post_id"); 
        $.ajax({
            type: "POST",
            url: "".concat('/likes-api-post/', post_id,'/'),
            data: {"post_id": post_id, 'csrfmiddlewaretoken': csrf_token },
            dataType: 'json',
            success: function(data){
                let like_button =  $(like_id),
                initial_value = parseInt(localStorage.getItem("initial_value"));
                status_of_button = $(like_id).attr('name');

                if (data.status == true && num_of_likes === initial_value && status_of_button == 'like-button-not-liked'){  
                    console.log('liked!')
                    like_button.css('color','#0275d8');
                    num_of_likes += 1;
                    document.getElementById(''.concat('span', post_id)).textContent=(num_of_likes);

                } else if (data.status == false && num_of_likes === (initial_value + 1) && status_of_button === 'like-button-not-liked'){
                    console.log('unliked!')
                    like_button.css('color','grey');
                    num_of_likes -= 1;
                    document.getElementById(''.concat('span', post_id)).textContent=(num_of_likes);
                                        
                } else if (data.status == false && num_of_likes === initial_value && status_of_button == 'like-button-liked'){
                    console.log('liked!')
                    like_button.css('color','grey');
                    num_of_likes -= 1;
                    document.getElementById(''.concat('span', post_id)).textContent=(num_of_likes);
                } else if (data.status == true && num_of_likes === (initial_value - 1) && status_of_button == 'like-button-liked'){
                    console.log('unliked!')
                    like_button.css('color','#0275d8');
                    num_of_likes += 1;
                    document.getElementById(''.concat('span', post_id)).textContent=(num_of_likes);
                }           
            }
        });
        event.stopImmediatePropagation();
        return false;
    })
    })