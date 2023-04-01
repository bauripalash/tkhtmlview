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
                       <strong>This is a bold text</strong>
                       <em>This is a italic text</em>
                       <img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"></img>
                       <ul>
                        <li> One </li>
                        <ul>
                            <li> One.Zero </li>
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
      <th>T Header 1</th>
      <th>T Header 2</th>
    </tr>
    <tr>
      <td>ABC</td>
      <td>123</td>
    </tr>
    <tr>
      <td>DEF</td>
      <td>456</td>
    </tr>

</table>
                       """,
)
html_label.pack(fill="both", expand=True)
html_label.fit_height()
root.mainloop()
