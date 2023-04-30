let sliders = document.querySelectorAll('.my-slider');
let controls = document.querySelectorAll('#control');
let prev = document.querySelectorAll('.prev');
let next = document.querySelectorAll('.next');
for (let i = 0; i < sliders.length; i++) {
    tns({
        container: sliders[i],
        controlsContainer: controls[i],
        prevButton: prev[i],
        nextButton: next[i],

        // options here
        items: 8,
        gutter: 20,
        slideBy: 1,


        controlsPosition: "bottom",
        navPosition: "bottom",
        mouseDrag: true,
        autoplay: true,
        autoplayButtonOutput: false,

        responsive: {
            0: {
                items: 4,
                nav: false
            },
            768: {
                items: 6,
                nav: true
            },
            1440: {
                items: 8
            }
        }

    });
};

/* 1 instance */
// var slider = tns({
//     container: ".my-slider",
//     items: 6,
//     gutter: 20,
//     slideBy: 1,
//     controlsPosition: "bottom",
//     control: false,
//     navPosition: "bottom",
//     mouseDrag: true,
//     autoplay: true,
//     autoplayButtonOutput: false,
//     controlsContainer: "#custom-control",
//     responsive: {
//         0: {
//             items: 4,
//             nav: false
//         },
//         768: {
//             items: 6,
//             nav: true
//         },
//         1440: {
//             items: 6
//         }
//     }
//     // mode: 'gallery',
//     // speed: 2000,
//     // animateIn: "scale",
//     // controls: false,
//     // nav: false,
//     // edgePadding: 20,
//     // loop: false,
// });