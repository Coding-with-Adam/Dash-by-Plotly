var BillionFormatter = function(value) {
    var val = Math.abs(value);
    if (val >= 1000000) {
      val = (val / 1000000000).toFixed(1) + " B";
    }
    return val;
  };

  var GigatonneFormatter = function(value) {
    var val = Math.abs(value);
    if (val >= 1000000) {
      val = (val / 1000000000).toFixed(1) + " Gt";
    }
    return val;
  };