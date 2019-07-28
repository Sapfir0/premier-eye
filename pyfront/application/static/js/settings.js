

document.addEventListener("DOMContentLoaded", async () => {
    const algorithm = document.querySelector(".algorithm")
    const oldFrames = document.querySelector(".oldFrames")
    const carDetector = document.querySelector(".carDetector")

    algorithm.addEventListener("click", () => {
        console.log(algorithm.checked);
    })

    oldFrames.addEventListener("click", () => {
    })

    carDetector.addEventListener("click", () => {
    })

    // запускать докер образ с аргументами, которые можно взять отсюда

})