const getFebDays = (year) => (
        (year % 4 == 0 && year % 100 != 0 && year % 400 != 0) || 
        (year % 100 == 0 && year % 400 == 0)
    ) ? 29 : 28;

let calendar = document.querySelector('.calendar');
const month_names = [
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December',
];
let month_picker = document.querySelector('#month-picker');
const timeFormate = document.querySelector('.time-formate');
const dateFormate = document.querySelector('.date-formate');
const dayshow = document.querySelector('.date-time-formate');
const foot = document.querySelector('.calendar-footer');
const height = screen.availHeight - calendar.offsetTop * 2 - 30 - 90;

month_picker.onclick = () => {
    month_list.classList.remove('hideonce');
    month_list.classList.remove('hide');
    month_list.classList.add('show');
    timeFormate.classList.remove('showtime');
    timeFormate.classList.add('hidetime');
    dayshow.classList.remove('showtime');
    dayshow.classList.add('hidetime');
    dateFormate.classList.remove('showtime');
    dateFormate.classList.add('hidetime');
};
const calendar_days = document.querySelector('.calendar-days');
const calendar_header_year = document.querySelector('#year');

const generateCalendar = (month,year) => {
    calendar_days.innerHTML = '';
    let days_of_month = [
        31,
        getFebDays(year),
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    ];
    month_picker.innerHTML = month_names[month];
    calendar_header_year.innerHTML = year;
    let first_day = new Date(year,month);
    for(let j=days_of_month[month],i=1-first_day.getDay(),
    w=[currentDate.getDate(),currentDate.getFullYear(),currentDate.getMonth()];
    i<=j;i++){
        let day = document.createElement('div');
        if(i>0){
            day.innerHTML = i;
            if(i==w[0]&&year==w[1]&&month==w[2])day.classList.add('current-date');
        }else{
            day.classList.add('not-in-date');
        }
        calendar_days.appendChild(day);
    }
    foot.style.height = height - (calendar.scrollHeight - foot.scrollHeight) + 'px';//put generateCalendar() after month_names-209
};
let month_list = calendar.querySelector('.month-list');

document.querySelector('#pre-year').onclick = () => {
    --currentYear.value;
    generateCalendar(currentMonth.value, currentYear.value);
};
document.querySelector('#next-year').onclick = () => {
    ++currentYear.value;
    generateCalendar(currentMonth.value, currentYear.value);
};

let currentDate = new Date();
let currentMonth = {value : currentDate.getMonth()};
let currentYear = {value : currentDate.getFullYear()};
document.getElementById('today').onclick = () => generateCalendar(currentDate.getMonth(), currentDate.getFullYear());

month_names.forEach((e, index) => {
    let month = document.createElement('div');
    month.innerHTML = `<div>${e}</div>`;
    month_list.append(month);
    month.onclick = () => {
        currentMonth.value = index;
        generateCalendar(currentMonth.value, currentYear.value);
        month_list.classList.remove('show');
        month_list.classList.add('hide');
        timeFormate.classList.remove('hidetime');
        timeFormate.classList.add('showtime');
        dateFormate.classList.remove('hidetime');
        dateFormate.classList.add('showtime');
        dayshow.classList.remove('hidetime');
        dayshow.classList.add('showtime');
    };
});
month_list.classList.add('hideonce');

generateCalendar(currentMonth.value, currentYear.value);

function showtodate(){
    const currshowDate = new Date();
    const showCurrentDateOption = {
        year : 'numeric',
        month : 'long',
        day : 'numeric',
        weekday : 'long',
    };
    dateFormate.textContent = new Intl.DateTimeFormat(
        'en-US',
        showCurrentDateOption
    ).format(currshowDate);
    return(currshowDate.getDate());
};
let thedate = showtodate();
setInterval(() => {
    const timer = new Date();
    const option = {
        hour : 'numeric',
        minute : 'numeric',
        second : 'numeric',
    };
    const formateTimer = new Intl.DateTimeFormat('en-us', option).format(timer);
    let time = `${`${timer.getHours()}`.padStart(
        2,
        '0'
    )}:${`${timer.getMinutes()}`.padStart(
        2,
        '0'
    )}:${`${timer.getSeconds()}`.padStart(2,'0')}`;
    timeFormate.textContent = formateTimer;
    if(thedate != timer.getDate()) thedate=showtodate();
},1000);