document.addEventListener(
"DOMContentLoaded", () => {

    const hello =
    document.getElementById(
    "helloText");

    const welcome =
    document.getElementById(
    "welcomeText");

    const tagline =
    document.getElementById(
    "taglineText");

    const intro =
    document.getElementById(
    "introScreen");

    const login =
    document.getElementById(
    "loginSection");


    // HELLO LETTER BY LETTER

    const text = "Hello";

    let index = 0;

    function typeHello(){

        if(index < text.length){

            hello.innerHTML +=
            text.charAt(index);

            index++;

            setTimeout(
            typeHello, 250);
        }
    }

    typeHello();


    // Welcome

    setTimeout(() => {

        welcome.classList
        .add("show");

    }, 1800);


    // Tagline

    setTimeout(() => {

        tagline.classList
        .add("show");

    }, 2600);


    // Fade all

    setTimeout(() => {

        intro.style.opacity =
        "0";

    }, 5200);


    // Show login

    setTimeout(() => {

        intro.style.display =
        "none";

        login.classList
        .add("show");

    }, 6500);


    // Login Demo

    document
    .getElementById(
    "loginBtn")

    .addEventListener(
    "click", () => {

        const username =
        document
        .getElementById(
        "username")
        .value.trim();

        const password =
        document
        .getElementById(
        "password")
        .value.trim();

        const error =
        document
        .getElementById(
        "loginError");

        if(
            username ===
            "admin"
            &&
            password ===
            "admin123"
        ){

            error.textContent =
            "";

            window.location.href =
                      "/app/dashboard";
        }

        else{

            error.textContent =
            "Invalid Username or Password";
        }
    });
});