import tkinter as tk
from tkhtmlview import HTMLScrolledText

root = tk.Tk()
root.geometry("780x640")
html_label = HTMLScrolledText(
    root,
    html="""
      <h1 style="color: red; text-align: center"> Hello World </h1>
      <h2> Smaller </h2>
      <h3> Little Smaller </h3>
      <h4> Little Little Smaller </h4>
      <h5> Little Little Little Smaller </h5>
      <h6> Little Little Little Little Smaller </h6>
      <b>This is a Bold text</b><br/>
      <strong>This is an Important text</strong><br/>
      <i>This is a Italic text</i><br/>
      <em>This is a Emphasized text</em><br/>
      <em>This is a <strong>Strong Emphasized</strong>   text   </em>.<br/>
      <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"></img>
      <ul>
      <li> One </li>
        <ul>
            <li> One.Zero </li>
            <li> One.One </li>
        </ul>
      <li> Two </li>
      <li> Three </li>
      <li> Four </li>
      </ul>

      <h3> Paragraph </h3>
      <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut quam sapien. Maecenas porta tempus mauris sed ullamcorper. Nulla facilisi. Nulla facilisi. Mauris tristique ipsum et efficitur lobortis. Sed pharetra ipsum non lacinia dignissim. Ut condimentum vulputate sem eget scelerisque. Curabitur ornare augue enim, sed volutpat enim finibus id. </p>

      <h3>Table</h3
      <table>
          <tr>
            <th style="background-color: silver">T Header 1</th>
            <th style="background-color: silver">T Header 2</th>
          </tr>
          <tr>
            <td>ABC</td>
            <td><em>123</em></td>
          </tr>
          <tr>
            <td>DEF</td>
            <td><i>456</i></td>
          </tr>
      </table>

      <h3> Preformatted text: spaces and newlines preserved </h3>
      <pre style="font-family: Consolas; font-size: 80%">
<b>Tags      Attributes          Notes</b>
a         style, <span style="color: RoyalBlue">href         </span>-
img       <u>src</u>, width, height  <i>experimental</i>
ol        <span style="color: Tomato">style, type         </span>-
ul        <i>style               </i>bullet glyphs only
div       style               -
      </pre>

      <h3> Code: spaces and newlines ignored </h3>
      <code style="font-family: Consolas; font-size: 80%">
<b>Tags      Attributes          Notes</b><br/>
a         style, <span style="color: RoyalBlue">href         </span>-
img       <u>src</u>, width, height  <i>experimental</i>
ol        <span style="color: Tomato">style, type         </span>-
ul        <i>style               </i>bullet glyphs only
div       style               -
      </code>

    """,
)
html_label.pack(fill="both", expand=True)
html_label.fit_height()
root.mainloop()
