<h1>MindMetrics</h1>

<p>This project was developed during Megathon 2024, a premier hackathon organized by E-Cell IIIT Hyderabad, aiming to foster student innovation and entrepreneurship.</p>

<h2>Project Overview</h2>

<p>This project focuses on developing an NLP-based solution to automatically extract, classify, and analyze mental health concerns from user input. The solution includes polarity detection, keyword extraction (NER), concern classification, intensity scoring, and a timeline-based sentiment shift analysis. (<a href="https://megathon.in/problem_statements?utm_source=chatgpt.com">megathon.in</a>)</p>

<h2>Features</h2>

<ul>
  <li><strong>Data Analysis:</strong> Scripts for analyzing mental health data, utilizing datasets such as <code>mental_health_data.csv</code> and <code>dataset.csv</code>.</li>
  <li><strong>Web Interface:</strong> A Flask-based web application (<code>app.py</code>) providing a user-friendly interface for data visualization and interaction.</li>
  <li><strong>Logging:</strong> Implements logging mechanisms to track application behavior and errors, with logs stored in the <code>logs</code> directory.</li>
  <li><strong>Configuration Management:</strong> Utilizes a <code>config.py</code> file for managing application settings and configurations.</li>
  <li><strong>Containerization:</strong> Includes a <code>Dockerfile</code> and <code>docker-compose.yml</code> for easy deployment and scalability.</li>
</ul>

<h2>Installation</h2>

<p>To set up the project locally:</p>

<ol>
  <li><strong>Clone the repository:</strong>
    <pre><code>git clone https://github.com/JohnPrabhasith/Megathon_24.git</code></pre>
  </li>
  <li><strong>Navigate to the project directory:</strong>
    <pre><code>cd Megathon_24</code></pre>
  </li>
  <li><strong>Install dependencies:</strong>
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li><strong>Set up environment variables:</strong> Create a <code>.env</code> file in the root directory and define necessary environment variables as required by the application.</li>
</ol>

<h2>Usage</h2>

<p>To run the application:</p>

<pre><code>python app.py</code></pre>

<p>Access the web interface at <a href="http://localhost:5000">http://localhost:5000</a>.</p>

<h2>Contributing</h2>

<p>Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure adherence to the project's coding standards and include relevant tests for new features.</p>

<h2>License</h2>

<p>This project is licensed under the MIT License. See the <a href="LICENSE">LICENSE</a> file for details.</p>

<h2>Contact</h2>

<p>For any questions or feedback, please contact John Prabhasith at prabhasith0708@gmail.com.</p>

</body>
</html>
