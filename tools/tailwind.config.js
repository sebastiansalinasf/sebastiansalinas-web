module.exports = {
  content: [__dirname + '/../site/**/*.html'],
  theme: { extend: {
    colors: {
      navy:{950:'#06132A',900:'#0B1F3A',800:'#13294B',700:'#1C3660'},
      slate2:{500:'#6B7A8F',400:'#8A97A8',300:'#AEB8C5',100:'#E8ECF1'},
      copper:{600:'#9E5F28',500:'#B87333',400:'#C98A4E',300:'#D9A877'},
      paper:'#F7F5F1'},
    fontFamily:{serif:['"Cormorant Garamond"','Georgia','serif'],sans:['Inter','system-ui','sans-serif']}
  }}
}
