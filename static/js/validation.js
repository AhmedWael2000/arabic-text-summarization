const form = document.getElementById('form');
const email = document.getElementById('email');
const nationalID = document.getElementById('nationalID');
const fullname = document.getElementById('fullname');
const feedback = document.getElementById('feedback');
const phone = document.getElementById('phone');
const gov = document.getElementById('gov');
const file = document.getElementById('files');

form.addEventListener('submit', e => {
  
    if(!checkInputs()){
        e.preventDefault();
    }
    
}
);

function checkInputs() {
    var errors = 0;
//     // trim to remove the whitespaces
    const emailValue = email.value.trim();
    const fullnameValue = fullname.value.trim();
    const nationalIDValue = nationalID.value.trim();
    const feedbackValue = feedback.value.trim();
    const phoneValue = phone.value.trim();

    const govValue = gov.value.trim();
    
    if (fullnameValue === '') {
        setErrorFor(fullname, 'أدخل الاسم رباعي باللغة العربية');
        errors++;
    } else if(!isName(fullnameValue)){
        setErrorFor(fullname, ' أدخل الاسم رباعي باللغة العربية');
        errors++;
    }else {
        setSuccessFor(fullname);
    }

    if (nationalIDValue === '') {
        setErrorFor(nationalID, '(أربعة عشر رقم) أدخل الرقم القومي بشكل صحيح');
        errors++;
    } else if(!isID(nationalIDValue)){
        setErrorFor(nationalID, '(أربعة عشر رقم) أدخل الرقم القومي بشكل صحيح');
        errors++;
    }else{
        setSuccessFor(nationalID);
    }

    if (emailValue === '') {
        setErrorFor(email, 'أدخل البريد الإلكتروني بشكل صحيح');
        errors++;
    } else if (!isEmail(emailValue)) {
        setErrorFor(email, 'أدخل البريد الإلكتروني بشكل صحيح');
        errors++;
    } else {
        setSuccessFor(email);
    }
       
    if (phoneValue === '') {
        setErrorFor(phone, 'أدخل رقم الهاتف بشكل صحيح');
        errors++;
    }
     else if(!isNum(phoneValue)){
        setErrorFor(phone, 'أدخل رقم الهاتف بشكل صحيح');
        errors++;
    }
    else {
        setSuccessFor(phone);
    }
    if (feedbackValue === '') {
        setErrorFor(feedback, 'أضف مقترحك');
        errors++;
    } else {
        setSuccessFor(feedback);
    }

    if (govValue === '') {
        setErrorFor(gov, 'أضف محافظتك');
        errors++;
    } else {
        setSuccessFor(gov);
    }

    
    if (errors == 0)
        return true;
    else {
        return false;
    }

}

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = 'form-control error';
    small.innerText = message;
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function isEmail(email) {
    return /^\w+@\w+\.\w+$/.test(email);
}
function isNum(num) {
    return /^(\+2|2)?01[0-9]{9}$/.test(num);
}
function isID(num) {
    return /^[0-9]{14}$/.test(num);
}
function isName(num) {
    return /^[\u0600-\u06FF]+ [\u0600-\u06FF]+ [\u0600-\u06FF]+ [\u0600-\u06FF]+$/.test(num);
}
// 01 142212791
// function isNumber(num) {
//     return /^(+2){,1}01[0-9]{9}$/.test(num);
// }
