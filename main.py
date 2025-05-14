from kivy.utils import platform
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock

if platform == 'android':
    from jnius import autoclass, cast
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    WebView = autoclass('android.webkit.WebView')
    WebViewClient = autoclass('android.webkit.WebViewClient')
    LinearLayout = autoclass('android.widget.LinearLayout')
    ViewGroup = autoclass('android.view.ViewGroup')
    LayoutParams = autoclass('android.widget.LinearLayout$LayoutParams')

class WebBrowserApp(App):
    def build(self):
        self.url_bar = TextInput(text='https://www.google.com', size_hint_y=0.1, multiline=False)
        self.url_bar.bind(on_text_validate=self.load_url)

        # Navigation bar
        nav_bar = BoxLayout(size_hint_y=0.1)
        btn_back = Button(text='←')
        btn_back.bind(on_release=self.go_back)
        btn_fwd = Button(text='→')
        btn_fwd.bind(on_release=self.go_forward)
        btn_home = Button(text='🏚')
        btn_home.bind(on_release=self.go_home)
        btn_reload = Button(text='⟳')
        btn_reload.bind(on_release=self.reload)

        nav_bar.add_widget(btn_back)
        nav_bar.add_widget(btn_fwd)
        nav_bar.add_widget(btn_home)
        nav_bar.add_widget(btn_reload)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.url_bar)
        layout.add_widget(nav_bar)

        if platform == 'android':
            Clock.schedule_once(self.create_webview, 1)

        return layout

    def create_webview(self, dt):
        activity = PythonActivity.mActivity
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        self.webview.loadUrl(self.url_bar.text)

        layout = activity.findViewById(0x1020002)
        layout.removeAllViews()
        android_layout = LinearLayout(activity)
        android_layout.setOrientation(1)
        android_layout.addView(self.webview, LayoutParams(-1, 0, 1))
        activity.setContentView(android_layout)

    def load_url(self, instance):
        if platform == 'android':
            url = self.url_bar.text
            if not url.startswith(('http://', 'https://')):
                url = 'http://' + url
            self.webview.loadUrl(url)

    def go_back(self, instance):
        if platform == 'android' and self.webview.canGoBack():
            self.webview.goBack()

    def go_forward(self, instance):
        if platform == 'android' and self.webview.canGoForward():
            self.webview.goForward()

    def go_home(self, instance):
        if platform == 'android':
            self.url_bar.text = 'https://www.google.com'
            self.webview.loadUrl(self.url_bar.text)

    def reload(self, instance):
        if platform == 'android':
            self.webview.reload()

if __name__ == '__main__':
    WebBrowserApp().run()
