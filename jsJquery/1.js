 $("#tbody").on("click", ".edit_btn", function () {
        $("#myModal").modal("show");
        $("#btn_sub").text("saveUpdate");
        var tds = $(this).parent().parent().parent().parent().children("td").slice(0,4);
        var attr = [];
        tds.each(function () {
            var tdText = $(this).text();
            attr.push(tdText)
        });

        var modalInputs = $(".addMsg");
        var i = 0;
        modalInputs.each(function () {
            $(this).val(attr[i]);
            i++;
        });

        $("#btn_sub").on("click", function () {
            var ar=[];

            $(".addMsg").each(function () {
                ar.push($(this).val());

            });
            var i = 0;



             tds.each(function () {

               $(this).text(ar[i]);
               i++
           });

            $("#myModal").modal("hide");

        });

 });
//
//        var tds= $(this).parent().parent().parent().parent().children("td").slice(0,4);
//         tds.each(function () {
//             //alert($(this).text())
//             $(this).html("<input type='text' value=" + $(this).text() + ">")
//         });
//         $(this).text("保存");
//
//
//         $(this).removeClass("btn btn-success edit_btn");
//         $(this).addClass("btn btn-info saveBtn");
