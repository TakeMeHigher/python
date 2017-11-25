$(".head").on("mouseover", function () {
    $(this).next().slideDown();
});

$(".head").parent().on('mouseleave', function () {
    $(".head").next().slideUp();
})