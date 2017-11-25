$(function () {
    //头像预览
    $("#avatar_file").change(function () {
        var current_file = $(this)[0].files[0];
        var reader = new FileReader();

        reader.readAsDataURL(current_file);

        reader.onload = function () {
            $('#avatar_img')[0].src = this.result
        }

    });


    $('#submitBtn').click(function () {
        var data = new FormData();
        data.append("username", $("#username").val());
        data.append("nickname", $("#nickname").val());
        data.append("avatar", $("#avatar_file")[0].files[0]);
        data.append("email", $("#email").val());
        data.append("password", $("#password").val());
        data.append("phone", $("#phone").val());
        data.append("confirmPassword", $("#confirmPassword").val());

        /**先清除错误信息*/
        $(".pull-right").html(' ');
        $(".pull-right").parent().removeClass("has-error");

        $.ajax({
            url: '/reg/',
            type: 'POST',
            headers: {"X-CSRFToken": $.cookie('csrftoken')},
            data: data,
            contentType: false,
            processData: false,
            success: function (data) {
                data = JSON.parse(data);
                //校验成功
                if (data['flag']) {
                    window.location.href = "/login/";
                } else {
                    //校验失败
                    for (i in data['error']) {
                        $span = $("<span>");
                        $("#" + i).after($span);
                        $span.html(data['error'][i]).css("color", "red").addClass("pull-right");
                        $span.parent().addClass("has-error");
                        console.log(data['error'][i]);

                    }
                }

            }
        })

    })
})