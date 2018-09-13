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
    //顶栏隐藏
    let previousTop = 0;
    let currentTop = 0;
    let previousTime = 0;
    let nowTime = 0;
    let nav = $('.navbar:eq(0)');

    $(window).scroll(() => {
        nowTime = new Date().getTime()
        if (nowTime - previousTime < 50) {
            return false
        }

        currentTop = $(window).scrollTop();

        if (currentTop - previousTop > 50) {

            nav.attr('id') === 'nav-show' ? nav.attr('id', 'nav-hide') : null
        } else if (previousTop - currentTop > 50) {
            nav.attr('id') === 'nav-hide' ? $('.navbar:eq(0)').attr('id', 'nav-show') : null
        }

        previousTop = currentTop;
        previousTime = nowTime;
    })
})

$(() => {
    //回到顶部
    let backImg = $('#back')
    $(window).scroll(() => {
        currentTop = $(window).scrollTop()

        if(currentTop < 800 && backImg.is(':visible')){
            backImg.hide('fast')
        }else if(currentTop > 800 && !backImg.is(':visible')){
            backImg.show('fast')
        }
    })

    backImg.click((e) => {
        $("html, body").animate({scrollTop: 0}, 500)
    })
})