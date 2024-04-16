
  window.onload = function() {
    const search_bt = document.getElementById("search_bt");
    const clear_bt = document.getElementById("clear-results-button");
    clear_bt.style.visibility = "hidden";

    if (search_bt) {
      search_bt.addEventListener('click', function() {
        clear_bt.style.visibility = "visible";
      }); 
    }
  
  
    if (clear_bt) {
    clear_bt.addEventListener('click', function() {
      const resultsContainer = document.getElementsByClassName('daily_weather_results'); 
      console.log(resultsContainer);
      while(resultsContainer[0]) {
        resultsContainer[0].parentNode.removeChild(resultsContainer[0]);
    
    }
    clear_bt.style.visibility = "hidden";
  }); 
  }
}