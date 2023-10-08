const city = document.querySelector(".cities")

let tg = window.Telegram.WebApp

tg.expand()

const xhr = new XMLHttpRequest();
xhr.open("GET", "https://my.dnevnik76.ru/ajax/kladr/frontend/");
xhr.send();
xhr.responseType = "document";
xhr.onload = () => {
  if (xhr.status == 200) {
    const data = xhr.response;
    console.log(data.querySelector(".custom-select__list").children);
    for (const iterator of data.querySelector(".custom-select__list").children) {
        city.insertAdjacentHTML("beforeend",'<option value="'+iterator.dataset.value+'">'+iterator.innerHTML+'</option>')
    }
    city.insertAdjacentHTML("beforeend",'<option value="19000000000/3">Хакасия р-п</option>')
  }
};

city.addEventListener("change", (e)=>{
    if (e.target.value.split("/")[1]=="2"){
        if (document.querySelector(".points") != undefined){
            document.querySelector(".points").remove()
        }
        if (document.querySelector(".schools") != undefined){
            document.querySelector(".schools").remove()
        }

        const xhr = new XMLHttpRequest();
        xhr.open("GET", "https://my.dnevnik76.ru/ajax/kladr/frontend/"+e.target.value.split("/")[0]);
        xhr.send();
        xhr.responseType = "document";
        xhr.onload = () => {
            if (xhr.status == 200) {
                const data = xhr.response;
                city.insertAdjacentHTML("afterend", '<select class="points" id=""><option selected disabled hidden>Выберите н-п</option></select>')
                const points = document.querySelector(".points");
                for (const iterator of data.querySelector(".custom-select__list").children) {
                    points.insertAdjacentHTML("beforeend",'<option value="'+iterator.dataset.value+'">'+iterator.innerHTML+'</option>')
                }
                points.addEventListener("change", (event)=>{
                    schools(points, event.target.value)
                })
            }
        };
    }
    else{
        if (e.target.value == "19000000000/3"){
            //schools(city, e.target.value)
        }
        else{
            schools(city, e.target.value)
        }
    }
})


function schools(points, pointsId){
    if (document.querySelector(".schools") != undefined){
        document.querySelector(".schools").remove()
    }
    const xhr = new XMLHttpRequest();
    xhr.open("GET", "https://my.dnevnik76.ru/ajax/school/frontend/"+pointsId.split("/")[0]);
    xhr.send();
    xhr.responseType = "document";
    xhr.onload = () => {
        if (xhr.status == 200) {
            const data = xhr.response;
            points.insertAdjacentHTML("afterend", '<select class="schools" id=""><option selected disabled hidden>Выберите школу</option></select>')
            const schools = document.querySelector(".schools");
            for (const iterator of data.querySelector(".custom-select__list").children) {
                schools.insertAdjacentHTML("beforeend",'<option value="'+iterator.dataset.value+'">'+iterator.innerHTML+'</option>')
            }
        } 
    };
}


document.querySelector("button").addEventListener("click", ()=>{
    if ((document.querySelector(".schools") != undefined || city.value == "19000000000/3")
     && document.querySelector(".login").value != "" 
     && document.querySelector(".password").value != ""){
        let school;
        if (document.querySelector(".schools") != null){
            school = document.querySelector(".schools").value
        }
        else {
            school = 19000000000
        }
        let data = {
            login: document.querySelector(".login").value,
            password: document.querySelector(".password").value,
            school: school
        }
        
        tg.sendData(JSON.stringify(data))

        tg.close()
    }
})


