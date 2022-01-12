function startup() {
  var el = document.getElementsByTagName("canvas")[0];
  el.addEventListener("touchstart", handleStart, false);
  el.addEventListener("touchend", handleEnd, false);
  el.addEventListener("touchcancel", handleCancel, false);
  el.addEventListener("touchleave", handleLeave, false);
  el.addEventListener("touchmove", handleMove, false);
}

function handleStart(evt) {
    console.log('touchstart');
}

function handleEnd(evt) {
    console.log('touchend');
}
