<h1>Check files for unused imports and unused packages in requirements.txt</h1>
<h3>Has been optimized for speed</h3>

<div>
    <p>You need python3 and pandas to run this.</p>
</div>

<h3>Known limitation:</h3>
<p>If the requirement name is different from the import values then it will be missed. See <b>scikit-learn and sklearn</b>. I don't have an answer to that.</p>
<h3>Steps</h3>
<ol>
    <li>cd /Users/yashbehal/projects/doorstep-django</li>
    <li>Run 'pipdeptree > treefreeze.txt'
        <ul>
            <li>If I don't work run 'pip install pipdeptree' and run again</li>
        </ul>
    </li>
    <li>Remove what we just did
        <ol>
            <li>rm -rf pylinttest</li>
            <li>rm -rf lint_dir</li>
        </ol>
    </li>
    <li>Clone me into the dd repository
        <ul>
            <li>git clone https://github.com/travistheall/lint_dir</li>
        </ul>
    </li>
    <li>See image for python script set up</li>
    <li>Hit play</li>
    <li>Creates 2 files
        <ol>
            <li>not_in_requirements.csv: A csv file with all the packages that are used in the project, but not in requirements.txt</li>
            <ul>
                <li>math, os, project modules, ...</li>
            </ul>
            <li>requirements.csv: A csv file with all the packages from requirements.txt and 1 if used 0 if not</li>
        </ol>
    </li>
    <li>Let me know how this goes. It's sunday and I'm tired of working.</li>
</ol>

<h2>Pycharm Config To Run Script</h2>
<h4>Configure a python3 interpreter</h4>
<img src="https://user-images.githubusercontent.com/58260017/148442415-b7cb3297-4c36-4027-85df-53a3439ea147.png" />
