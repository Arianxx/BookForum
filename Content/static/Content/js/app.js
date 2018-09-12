$('.reply_btn').click(e => {
    // 点击回复按钮，添加mention到输入框，并跳转到输入框
    let ele = $(e.target)
    let mention = ' @' + ele.attr('data-user') + ' '
    let reply_box = $('#reply_box')[0]
    if (reply_box.value.indexOf(mention) === -1) {
        reply_box.value = mention + reply_box.value
    }

    location.hash = ''
    location.hash = '#reply_box'

    return false
})


$(() => {
    let previousTop = 0;
    let currentTop = 0;
    let previousTime = 0;
    let nowTime = 0;
    let nav = $('.navbar:eq(0)');

    $(window).scroll(() => {
        nowTime = new Date().getTime()
        if(nowTime - previousTime < 70){
            return false
        }

        currentTop = $(window).scrollTop();

        if(currentTop - previousTop > 100){

            nav.attr('id')==='nav-show'?nav.attr('id', 'nav-hide'):null
        } else if(previousTop - currentTop > 100) {
            nav.attr('id')==='nav-hide'?$('.navbar:eq(0)').attr('id', 'nav-show'):null
        }

        previousTop = currentTop;
        previousTime = nowTime;
    })
})