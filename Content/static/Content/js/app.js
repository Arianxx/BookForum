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