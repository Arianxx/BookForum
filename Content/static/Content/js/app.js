$('.reply_btn').click(e => {
    // 点击回复按钮，添加mention到输入框，并跳转到输入框
    let ele = $(e.target);
    let mention = ' @' + ele.attr('data-user') + ' ';
    let reply_box = $('#reply_box')[0];
    if (reply_box.value.indexOf(mention) === -1) {
        reply_box.value = mention + reply_box.value
    }

    location.hash = '';
    location.hash = '#reply_box';

    return false
});


$(function hideNavBar() {
    //顶栏隐藏
    let previousTop = 0;
    let currentTop = 0;
    let previousTime = 0;
    let nowTime = 0;
    let nav = $('.navbar:eq(0)');

    $(window).scroll(() => {
        nowTime = new Date().getTime();
        if (nowTime - previousTime < 50) {
            return true
        }

        currentTop = $(window).scrollTop();

        if (currentTop < 100) {
            nav.attr('id') === 'nav-hide' ? $('.navbar:eq(0)').attr('id', 'nav-show') : null
        } else if (currentTop - previousTop > 10) {

            nav.attr('id') === 'nav-show' ? nav.attr('id', 'nav-hide') : null
        } else if (previousTop - currentTop > 10) {
            nav.attr('id') === 'nav-hide' ? $('.navbar:eq(0)').attr('id', 'nav-show') : null
        }

        previousTop = currentTop;
        previousTime = nowTime;
    })
});

$(function backToTop() {
    //回到顶部
    let backImg = $('#back');
    $(window).scroll(() => {
        currentTop = $(window).scrollTop();

        if (currentTop < 800 && backImg.is(':visible')) {
            backImg.hide('fast')
        } else if (currentTop > 800 && !backImg.is(':visible')) {
            backImg.show('fast')
        }
    });

    backImg.click((e) => {
        $("html, body").animate({scrollTop: 0}, 500)
    })
});

class FixNav {
    constructor(ele, contrastEle) {
        if (ele.height() > contrastEle.height()) {
            let temp = contrastEle;
            contrastEle = ele;
            ele = temp
        }
        this.ele = ele;
        this.contrastEle = contrastEle;
        this.previousTop = 0;
        this.initialMulriple = contrastEle.width() / ele.width();

        this.upping = false;
        this.downing = true;
    }

    adaptWidth(e) {
        if ($(document).width() < 1200) {
            e.data.initialMulriple = 1;
            e.data.ele.css({
                'position': '',
                'margin-top': '',
                'top': '',
                'bottom': '',
            })
        } else if (e.data.initialMulriple < 1.1 && e.data.initialMulriple > 0.9) {
            e.data.initialMulriple = 2
        }
        e.data.ele.css('width', e.data.contrastEle.width() / e.data.initialMulriple)
    };

    toLowerBound() {
        const ele = this.ele;
        let nowTop = $(window).height() + $(window).scrollTop();
        let eleTop = ele.offset().top + ele.height();
        let temp = nowTop - eleTop;
        return temp > 0;
    };

    toUpperBound() {
        const ele = this.ele;
        let nowTop = $(window).scrollTop();
        let eleTop = ele.offset().top;
        let temp = nowTop - eleTop;
        // return temp < -45;
        return temp < 0;
    };

    isDownScroll() {
        let nowTop = $(window).scrollTop();
        let result = nowTop - this.previousTop;
        this.previousTop = nowTop;
        return result > 0;
    };

    fixedNav(arrow) {
        if ((this.downing && arrow === 'up') || (this.upping && arrow === 'down')) {
            return false
        }

        const ele = this.ele;
        let arrowWord = arrow === 'up' ? 'top' : 'bottom';
        const cssObj = {
            'position': 'fixed',
            'margin-top': '',
        };
        cssObj[arrowWord] = arrow === 'up' ? 60 : 0;
        ele.css(cssObj);
        ele.attr('arrow', arrow);
        ele.arrow = arrow;
    };

    unFixedNav() {
        const ele = this.ele;
        let position = ele.offset();
        const parentTop = ele.parent().offset().top;
        ele.css({
            "margin-top": position.top - parentTop,
            'position': 'relative',
            'top': '',
            'bottom': '',
        });
        ele.attr('arrow', '');
        delete ele.arrow
    };

    handleDownScroll() {
        this.downing = true;
        this.upping = false;

        if (this.ele.arrow === 'up') {
            this.unFixedNav()
        } else if (this.ele.offset().top + this.ele.height() + 150 > $(document).height()) {
            this.unFixedNav()
        } else if (!this.ele.arrow && this.toLowerBound()) {
            this.fixedNav('down')
        }
    }

    handleUpScroll() {
        this.upping = true;
        this.downing = false;

        if (this.ele.arrow === 'down') {
            this.unFixedNav()
        } else if (!this.ele.arrow && this.toUpperBound()) {
            this.fixedNav('up')
        }
    };

    run() {
        this.adaptWidth({data: this});
        $(window).resize(this, this.adaptWidth);

        $(window).scroll(() => {
            let gap = this.contrastEle.width() - this.ele.width();
            gap = gap < 0 ? -gap : gap;
            if (gap > 10) {
                if (this.isDownScroll()) {
                    this.handleDownScroll()
                } else {
                    this.handleUpScroll()
                }
            }
        })
    }
}

$(function fixRightNav() {
    //滚动到侧栏底部固定侧栏

    let leftContent = $('#left_content');
    let rightNav = $('.wrap-right-nav:eq(0)');

    new FixNav(rightNav, leftContent).run()
});

$(function fixLeftNav() {
    //左边栏

    let left = $('#book-left-nav');
    let right = $('#book-right-nav');
    new FixNav(left, right).run()
});