function setMyKeyDownListener() {
  window.addEventListener("keydown", function (event) {
    MyFunction(event.key);
  });
}

function MyFunction(the_Key) {
  // alert("Key pressed is: "+the_Key);
  var pic, pic1;
  switch (the_Key) {
    case "ArrowUp":
      pic = "images/arrow-up-active.png";
      document.getElementById("ArrUp").src = pic;
      break;
    case "ArrowDown":
      pic = "images/arrow-down-active.png";
      document.getElementById("ArrDown").src = pic;
      break;
    case "ArrowLeft":
      pic = "images/arrow-left-active.png";
      document.getElementById("ArrLeft").src = pic;
      break;
    case "ArrowRight":
      pic = "images/arrow-right-active.png";
      document.getElementById("ArrRight").src = pic;
      break;

    default:
      document.getElementById("ArrUp").src = "images/arrow-up.png";
      document.getElementById("ArrDown").src = "images/arrow-down.png";
      document.getElementById("ArrLeft").src = "images/arrow-left.png";
      document.getElementById("ArrRight").src = "images/arrow-right.png";
      break;
  }
  // document.getElementById("myImage").src = pic;
}
