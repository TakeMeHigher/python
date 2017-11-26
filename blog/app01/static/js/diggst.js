function foo() {
    $("#uperror").html(" ")
}

//点赞
$(".diggit").click(function () {

    $.ajax({
        url: "/blog/diggit/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            article_id: $("#article_id").html()
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.flag) {
                var val = parseInt($("#digg_count").html()) + 1;
                $("#digg_count").html(val)

            } else {
                $("#uperror").html(data.errors).css("color", "red");
                setTimeout(foo, 3000)
            }
        }
    })
});

//反对
$(".buryit").click(function () {
    $.ajax({
        url: "/blog/buryit/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            article_id: $("#article_id").html()
        },
        success: function (data) {
            if(!data){
                window.location.href="/login/"
            }
            data = JSON.parse(data);
            if (data.flag) {
                var val = parseInt($("#bury_count").html()) + 1;
                $("#bury_count").html(val)

            } else {
                $("#uperror").html(data.errors).css("color", "red");
                setTimeout(foo, 3000)
            }
        }
    })
});


function comment_error() {
    $("#commenterror").html('')
}

//提交评论
$("#subBtn").click(function () {
    content=null;
    if(parent_comment_id){
        var index=$("#comment_content").val().indexOf("\n");
        content=$("#comment_content").val().slice(index);
    }else{
      content=$("#comment_content").val();
    }
    $.ajax({
        url: "/blog/comment/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            content: content,
            article_id: $("#article_id").html(),
            parent_comment_id:parent_comment_id,
        },
        success: function (data) {
            data = JSON.parse(data);
            if (data.flag) {
                if ($(".layer").last().html()) {
                    floor = parseInt($(".layer").last().html()) + 1;
                } else {
                    floor = 1
                }
                nickname = $("#tbCommentAuthor").val();
                content = $("#comment_content").val();
                date = data.comment_time;
                var s = '<div class="commentItem" >\n' +
                    '                        <div class="feedbackManage">\n' +
                    '                            &nbsp;&nbsp;\n' +
                    '                            <span class="comment_actions">\n' +
                    '                          <a href="#" comment_id="'+comment_id+'" comment_name="'+comment_name+'">回复</a>\n' +
                    '                          <a href="#">引用</a>\n' +
                    '                      </span>\n' +
                    '                        </div>\n' +
                    '                        <div class="commentTile">\n' +
                    '                            <a href="#3762185" class="layer">' + floor + '楼</a>\n' +
                    '                            <span>' + date + '</span>\n' +
                    '                            <a href="">' + nickname + '</a>\n' +
                    '                        </div>\n' +
                    '                        <div class="commentContent">\n' +
                    '                            <div class="comment_body_content">\n' +
                    '                               ' + content + '\n' +
                    '                            </div>\n' +
                    '\n' +
                    '                            <div class="comment_vote">\n' +
                    '                                <a href="#" class="comment_digg">支持(0)</a>\n' +
                    '                                <a href="#" class="comment_bury">反对(0)</a>\n' +
                    '                            </div>\n' +
                    '                        </div>\n' +
                    '                    </div>';

                $("#comment_list").append(s)

                 $("#comment_content").val('')

            } else {
                $("#commenterror").html(data.errors);
                setTimeout(comment_error, 3000)
            }
        }

    })
});

//对评论进行评论
parent_comment_id=null;
comment_id=null;
comment_name=null;
$("#comment_list").on("click",".reply",function () {
        alert($(this).html());
       var  currentUser_nickname=$(this).attr("comment_name");
        content="@"+currentUser_nickname+'\n';
        alert(content)
        comment_id=$(this).attr("comment_id");
        comment_name=$(this).attr("comment_name");
        $("#comment_content").val(content);
        parent_comment_id=$(this).attr("comment_id")

});

//删除评论

$("#comment_list").on("click",".delComment",function () {
    parent_obj=$(this).parent().parent().parent()
    $.ajax({
        url:"/blog/delComment/",
        type:"POST",
        data:{
             csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            comment_id:$(this).attr("comment_id"),
        },

        success:function (data) {
           if(data=="ok"){

              parent_obj.remove()
           }
        }
    })
})

