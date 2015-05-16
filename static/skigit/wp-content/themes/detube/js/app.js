var myMessages = ['info', 'warning', 'error', 'success']; // define the messages types
$(document).ready(function () {
    // /static/skigit/wp-content/themes/detube/images/logo_placeholder1.png
    // /static/skigit/wp-content/themes/detube/images/noimage_user.jpg
    if ($("#id_logo_img").length == 1)
    {
        $("#id_logo_img").attr("onchange", "logo_imgURL(this);");
    }
    if ($("#id_profile_img").length == 1)
    {
        $("#id_profile_img").attr("onchange", "profile_imgURL(this);");
    }

    // Code added by mitesh for skigit like/unlike

    var csrftoken = getCookie('csrftoken');

    var $jqlike = jQuery.noConflict();
    $jqlike(".like_unlike").click(function ()
    {
        //alert(csrftoken);
        var user_id = $jqlike(this).attr('data-userid');
        if (user_id == 1)
        {
            var skigit_id = $jqlike(this).attr('data-pid');
            var post_id = $jqlike(this).attr('id');
            $.ajax({
                type: "POST",
                url: "/skigit_like/",
                data: {'skigit_id': skigit_id, 'csrfmiddlewaretoken': csrftoken},
                //dataType: "text",
                success: function (response)
                {
                    alert(response.message);
                    //alert('You liked this')
                    if (response.is_liked == 1)
                    {
                        $jqlike("#" + post_id).removeClass("like");
                        $jqlike("#" + post_id).addClass("liked");
                        $jqlike("#likecount" + skigit_id).html(response.like_count);
                    }
                    else
                    {
                        $jqlike("#" + post_id).removeClass("liked");
                        $jqlike("#" + post_id).addClass("like");
                        $jqlike("#likecount" + skigit_id).html(response.like_count);
                    }
                },
                error: function (rs, e)
                {
                    alert("Please try again to like this skigit");
                }
            });
        }
        else
        {
            alert("Please login first to like Skigit");
        }
    });

    // End of code added by mitesh for skigit like/unlike

    $(".showdropdown").click(function () {

        if ($('.head_share_popupbox'))
            $('.head_share_popupbox').css("display", "none"); //sharebox
        if ($(".joinTooltip_content"))
            $(".joinTooltip_content").css("display", "none"); //joinbox
        if ($('.head_share_favpopup'))
            $('.head_share_favpopup').css("display", "none"); //fav sharebox
        if ($('.invitebox'))
            $('.invitebox').css("display", "none"); //friend invite
        if ($('.head_share_origin'))
            $('.head_share_origin').css("display", "none"); //origin sharebox
        if ($('#head_notification_popup'))
            $('#head_notification_popup').css("display", "none"); //notifications
        if ($('#head_frireq_popup'))
            $('#head_frireq_popup').css("display", "none"); //friend request
        if ($('#head_email_popup'))
            $('#head_email_popup').css("display", "none"); //emails
        if ($('.my_skigitt_popupbox'))
            $('.my_skigitt_popupbox').css("display", "none"); //popup statistics

        if ($(this).next().css('display') == 'none')
            $(this).next().slideDown("fast").css("display", "block");
        else
            $(this).next().slideUp("fast");
    });
    $(".dropdown-content").mouseover(function () {

        //alert('mrphpguru');
    });
    $(".dropdown-content").mouseleave(function () {
        if ($(".dropdown-content").css('display') == 'none')
        {
            //alert('none');
        }
        else
        {
            if ($("#head_share_popuploop11").css('display') == 'none')
            {
                $(".dropdown-content").slideUp("fast");
            }


        }

        //$().slideUp("fast");
        //alert('mrphpguru latestvideos');
    });

    hideAllMessages();
    var messagesHeights = new Array(); // this array will store height for each
    to = 0;
    // Show message

    for (var i = 0; i < myMessages.length; i++)
    {
        //alert(i);
        //$('.' + myMessages[i]).animate({top: "0"}, 500);
        if ($('.' + myMessages[i]).length > 0)
        {
            $('.' + myMessages[i]).show();
            $('.' + myMessages[i]).animate({top: to}, 1200);
            //messagesHeights[i] = $('.' + myMessages[i]).outerHeight();
            to += $('.' + myMessages[i]).outerHeight();
            //$('.' + myMessages[i]).css(top, +messagesHeights[i]); //move element outside viewport	  
        }

        showMessage(myMessages[i]);
    }

    // When message is clicked, hide it
    $('.message').click(function () {
        $(this).animate({top: -$(this).outerHeight()}, 500);
    });

    setTimeout(function () {
        hidemsg();
    }, 12000)
});//main document ready function


/* javascript functions  */


function hidemsg(){
    var messagesHeights = new Array(); // this array will store height for each
    to = 0;
    // Show message

    for (var i = 0; i < myMessages.length; i++)
    {
        //alert(i);
        //$('.' + myMessages[i]).animate({top: "0"}, 500);
        if ($('.' + myMessages[i]).length > 0)
        {
            //$('.' + myMessages[i]).show();
            to += $('.' + myMessages[i]).outerHeight();
            $('.' + myMessages[i]).animate({top: -to}, 1200);
            
            //$(this).animate({top: -$(this).outerHeight()}, 500);
            //messagesHeights[i] = $('.' + myMessages[i]).outerHeight();
            
            //$('.' + myMessages[i]).css(top, +messagesHeights[i]); //move element outside viewport	  
        }

        showMessage(myMessages[i]);
    }
} 
function hideAllMessages()
{
    var messagesHeights = new Array(); // this array will store height for each

    for (i = 0; i < myMessages.length; i++)
    {
        messagesHeights[i] = $('.' + myMessages[i]).outerHeight();
        $('.' + myMessages[i]).css('top', -messagesHeights[i]); //move element outside viewport	  
    }
}

function showMessage(type)
{
    $('.' + type + '-trigger').click(function () {
        hideAllMessages();
        alert(type);
        $('.' + type).animate({top: "0"}, 500);
    });
}


function logo_imgURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#logo_img')
                    .attr('src', e.target.result);
            //.width(150)
            //.height(200);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function profile_imgURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#profile_img')
                    .attr('src', e.target.result);
            //.width(150)
            //.height(200);
        };

        reader.readAsDataURL(input.files[0]);
    }
}


// Code added by mitesh for skigit like  unlike

function getCookie(name)
{
    var cookieValue = null;
    if (document.cookie && document.cookie != '')
    {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++)
        {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// End of code added for skigit like unlike