const app = getApp()

Page({
  data: {
    output_img_url: ''
  },
  load_img: function() {
    var refresh_data = (data) => {
      this.setData(data)
    }
    wx.chooseImage({
      success: function (res) {
        wx.showLoading({
          'title': 'processing'
        })

        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: app.globalData.server_url + 'api',
          filePath: tempFilePaths[0],
          name: 'img',
          complete: function(res) {
            wx.hideLoading()
          },
          success: function (res) {
            var data = JSON.parse(res.data)
            refresh_data({
              'output_img_url': app.globalData.server_url + data['url']
            })
          },
          fail: function (res) {
            var data = res.data
            console.log('failed')
            console.log(data)
          }
        })
      }
    })
  }
})
