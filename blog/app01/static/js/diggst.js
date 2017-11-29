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

            if (!data) {
                window.location.href = "/login/"
            }

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
            if (!data) {
                window.location.href = "/login/"
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
    editor.sync()
    if ($("#comment_content").val().charAt(0)!= "@") {
        parent_comment_id = null
    }
    var content = null;
    if (parent_comment_id) {
        var index = $("#comment_content").val().indexOf("\n");
        content = $("#comment_content").val().slice(index + 1);
    } else {
        content = $("#comment_content").val();
    }
    $.ajax({
        url: "/blog/comment/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            content: content,
            article_id: $("#article_id").html(),
            parent_comment_id: parent_comment_id
        },
        success: function (data) {
            if (!data) {
                window.location.href = "/login/"
            }
            data = JSON.parse(data);
            if (data.flag) {
                if ($(".layer").last().html()) {
                    floor = parseInt($(".layer").last().html()) + 1;
                } else {
                    floor = 1
                }
                nickname = $("#tbCommentAuthor").val();
                date = data.comment_time;
                var s = null;
                if (parent_comment_id) {
                    s = '<div class="commentItem" >\n' +
                        '                        <div class="feedbackManage">\n' +
                        '                            &nbsp;&nbsp;\n' +
                        '                            <span class="comment_actions">\n' +
                        '                          <a class="reply" comment_id="' + data.comment_id + '" comment_name="' + nickname + '">回复</a>\n' +
                        '                          <a href="#">引用</a>\n' +
                        '                      </span>\n' +
                        '                        </div>\n' +
                        '                        <div class="commentTile">\n' +
                        '                            <a href="#3762185" class="layer">' + floor + '楼</a>\n' +
                        '                            <span>' + date + '</span>\n' +
                        '                            <a href="">' + nickname + '</a>\n' +
                        '                        </div>\n' +
                        '                        <div class="commentContent">\n' +
                        '                            <div> <a href="" >@' + data.parent_comment_nickname + '</a></div><div class="comment_body_content">\n' +
                        '                               ' + content + '\n' +
                        '                            </div>\n' +
                        '\n' +
                        '                            <div class="comment_vote">\n' +
                        '                                <a  class="comment_digg" comment_id="' + data.comment_id + '">支持(0)</a>\n' +
                        '                                <a href="#" class="comment_bury">反对(0)</a>\n' +
                        '                            </div>\n' +
                        '                        </div>\n' +
                        '                    </div>';
                }

                else {
                    s = '<div class="commentItem" >\n' +
                        '                        <div class="feedbackManage">\n' +
                        '                            &nbsp;&nbsp;\n' +
                        '                            <span class="comment_actions">\n' +
                        '                          <a class="reply" comment_id="' + data.comment_id + '" comment_name="' + nickname + '">回复</a>\n' +
                        '                          <a href="#">引用</a>\n' +
                        '                      </span>\n' +
                        '                        </div>\n' +
                        '                        <div class="commentTile">\n' +
                        '                            <a href="#3762185" class="layer">' + floor + '楼</a>\n' +
                        '                            <span>' + date + '</span>\n' +
                        '                            <a href="" style="color:#337ab7;">' + nickname + '</a>\n' +
                        '                        </div>\n' +
                        '                        <div class="commentContent">\n' +
                        '                            <div class="comment_body_content">\n' +
                        '                               ' + content + '\n' +
                        '                            </div>\n' +
                        '\n' +
                        '                            <div class="comment_vote">\n' +
                        '                                <a  class="comment_digg" comment_id="' + data.comment_id + '">支持(<span>0</span>)</a>\n' +
                        '                                <a href="#" class="comment_bury">反对(<span>0</span>)</a>\n' +
                        '                            </div>\n' +
                        '                        </div>\n' +
                        '                    </div>';
                }

                // var s = '<div class="commentItem" >\n' +
                //     '                        <div class="feedbackManage">\n' +
                //     '                            &nbsp;&nbsp;\n' +
                //     '                        </div>\n' +
                //     '                        <div class="commentTile">\n' +
                //     '                            <a href="#3762185" class="layer">' + floor + '楼</a>\n' +
                //     '                            <span>' + date + '</span>\n' +
                //     '                            <a href="">' + nickname + '</a>\n' +
                //     '                        </div>\n' +
                //     '                        <div class="commentContent">\n' +
                //     '                            <div class="comment_body_content">\n' +
                //     '                               ' + content + '\n' +
                //     '                            </div>\n' +
                //     '\n' +
                //     '                        </div>\n' +
                //     '                    </div>';

                $("#comment_list").append(s);

                $("#comment_content").val('');
                parent_comment_id = null;
                editor.html('')

            } else {
                $("#commenterror").html(data.errors);
                setTimeout(comment_error, 3000)
            }
        }

    })
});

//对评论进行评论
parent_comment_id = null;
$("#comment_list").on("click", ".reply", function () {
    var currentUser_nickname = $(this).attr("comment_name");
    alert(currentUser_nickname)
    comment_id = $(this).attr("comment_id");
    // $("#comment_content").val("@" + currentUser_nickname + "\n");
    //editor.html("@" + currentUser_nickname + "\n");
    //$("#comment_content").focus();
    //editor.focus();
    editor.html('');//清空原有内容
    editor.focus();//编辑器获得焦点
    editor.appendHtml("@" + currentUser_nickname + "<br>")
    parent_comment_id = $(this).attr("comment_id");


});

//删除评论
$("#comment_list").on("click", ".delComment", function () {
    parent_obj = $(this).parent().parent().parent()
    $.ajax({
        url: "/blog/delComment/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            comment_id: $(this).attr("comment_id"),
        },

        success: function (data) {
            if (data == "ok") {

                parent_obj.remove()
            }
        }
    })
});


//获取评论树
article_id = $("#article_id").html();
$.ajax({
    url: "/blog/commentTree/" + article_id + "/",
    success: function (data) {
        data = JSON.parse(data);
        var s = showCommentTree(data);
        $("#commentTree").append(s);
    }
});

//展开评论树
function showCommentTree(comment_list) {
    var html = '';
    $.each(comment_list, function (index, comment_dict) {
        create_time = comment_dict.create_time.slice(0, 19);
        var content = comment_dict["content"];
        var comment_str = '<div>\n' +
            '                        <span> <a>' + comment_dict.user__nickname + '</a></span>发表于<a>' + create_time + '</a>\n' +
            '                    </div><div class="comment">\n' +
            '                     <div class="content">' + content + '</div>';

        if (comment_dict["children_comment"]) {
            var child_str = showCommentTree(comment_dict["children_comment"]);
            comment_str += child_str
        }
        comment_str += "</div>";
        html += comment_str
    });

    return html

}


//评论点赞
$("#comment_list").on("click", ".comment_digg", function () {
    span_obj = $(this).children().first();
    upcount = parseInt(span_obj.html());
    $.ajax({
        url: "/blog/commentDigg/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            comment_id: $(this).attr("comment_id")
        },
        success: function (data) {
            data = JSON.parse(data);

            if (data.flag) {
                span_obj.html(upcount + 1);
                data.flag = false
            } else {
                alert(data.error);

            }
        }
    });
});


KindEditor.ready(function (K) {
    window.editor = K.create('#comment_content', {
        width: '700px',
        height: '300px',
        uploadJson: "/backManage/uploadFile/",
         extraFileUploadParams: {
                    csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val()
                },
        items: [
            'source', 'wordpaste', 'justifyfull', 'fontname', 'fontsize', '|', 'forecolor', 'hilitecolor', 'bold',
            'italic', 'image', 'link', 'emoticons'
        ]
    });
});

