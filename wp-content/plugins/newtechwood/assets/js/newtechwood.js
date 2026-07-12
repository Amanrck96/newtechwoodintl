var $ = jQuery;
var scale = 1; // 初始缩放比例
const minScale = 0.5;
const maxScale = 5;
$(document).on('click', '[data-show-img]', function () {
    // 这里可以安全处理动态添加的元素
    const imgUrl = $(this).attr('data-show-img');
    const imageTitle = $(this).attr('data-show-title');
    $('.show-title').text(imageTitle);
    console.log('Clicked:', imgUrl);
    $('.show-box').css('bottom', '0')
    $('body').css('overflow-y', 'hidden')
    $('.show-div > iframe').hide();
    $('.show-div > img').attr('src', imgUrl);
    $('.show-div > img').show();
});
$(document).on('click', '[data-show-video]', function () {
    // 这里可以安全处理动态添加的元素
    const videoUrl = $(this).attr('data-show-video');
    const videoTitle = $(this).attr('data-show-title');
    $('.show-title').text(videoTitle);
    console.log('Clicked:', videoUrl);
    $('.show-box').css('bottom', '0')
    $('body').css('overflow-y', 'hidden')
    $('.show-div > img').hide();
    $('.show-div > iframe').attr('src', videoUrl);
    $('.show-div > iframe').show();
});
$('.close-show-box').click(() => {
    $('.show-box').css('bottom', '-100%')
    $('body').css('overflow-y', 'auto')
    scale = 1;
    $('.show-div > img').attr('src', '');
    $('.show-div > iframe').attr('src', '');
    $('.show-title').text('');
    $('.show-div > img').hide();
    $('.show-div > iframe').hide();
})


$('.show-div').on('wheel', function (e) {
    e.preventDefault(); // 阻止页面滚动

    const delta = e.originalEvent.deltaY;

    if (delta < 0) {
        // 向上滚，放大
        scale *= 1.1;
    } else {
        // 向下滚，缩小
        scale /= 1.1;
    }

    // 限制缩放范围
    scale = Math.min(maxScale, Math.max(minScale, scale));

    $(this).find('img').css('transform', `scale(${scale})`);
});
$('[data-name="mfiles"]').addClass('mfiles-box');


function resNumberHtml(el, number, unit) {
    number = number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    el.html('<p>' + number + ' ' + (unit || '') + '</p>');
}

function animateNumber(el, from, to, unit, duration = 2000) {
    let startTime = null;

    function step(timestamp) {
        if (!startTime) startTime = timestamp;
        const progress = Math.min((timestamp - startTime) / duration, 1);
        const current = Math.floor(progress * (to - from) + from);
        resNumberHtml(el, current, unit);
        if (progress < 1) {
            requestAnimationFrame(step);
        }
    }

    requestAnimationFrame(step);
}

// 判断元素是否在视口中
function isInViewport(el) {
    const rect = el.getBoundingClientRect();
    return rect.top < window.innerHeight && rect.bottom > 0;
}

// 标记已触发过的元素，防止重复执行动画
const animatedSet = new Set();

function checkAndAnimate() {
    $('[animate-number="true"]').each(function () {
        const el = $(this)[0]; // 原生 DOM 元素
        if (isInViewport(el) && !animatedSet.has(el)) {
            animatedSet.add(el); // 标记为已动画
            const $el = $(this);
            const countFrom = parseInt($el.data('number-from'));
            const countTo = parseInt($el.data('number-to'));
            const countUnit = $el.data('number-unit');
            animateNumber($el, countFrom, countTo, countUnit);
        }
    });
}

// 初次检查 + 滚动监听
$(document).ready(function () {
    checkAndAnimate();
    $(window).on('scroll resize', checkAndAnimate);

    const $filter = $('.gallery-filter');
    if($filter.length > 0){
        const stickyTop = $filter.offset().top;

        $(window).on('scroll', function () {
            if ($(window).scrollTop() + 114 >= stickyTop) {
                $filter.addClass('stuck');
            } else {
                $filter.removeClass('stuck');
            }
        });
    }
    
});