function foo() {
    $("#uperror").html(" ")
}


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


$(".buryit").click(function () {
    alert(123)
    $.ajax({
        url: "/blog/buryit/",
        type: "POST",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            article_id: $("#article_id").html()
        },
        success: function (data) {
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

$("#subBtn").click(function () {
    $.ajax({
        url: "/blog/comment/",
        type: "post",
        data: {
            csrfmiddlewaretoken: $("[name='csrfmiddlewaretoken']").val(),
            content: $("#comment_content").val(),
            article_id: $("#article_id").html(),

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
                date = data.comment_time
                var s = '<div class="commentItem" >\n' +
                    '                        <div class="feedbackManage">\n' +
                    '                            &nbsp;&nbsp;\n' +
                    '                            <span class="comment_actions">\n' +
                    '                          <a href="#">回复</a>\n' +
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
                    '                    </div>'

                $("#comment_list").append(s)


            } else {
                $("#commenterror").html(data.errors);
                setTimeout(comment_error, 3000)
            }
        }

    })
})