## Word Up!

As we near the end of a long Skill Track full boring things like movies, GIFs, and pyramids--the practicalities of life that, though perhaps necessary, are rather dull--you deserve some fun and games. So for this assignment, you will make a fun game!

## The Goal

The game you are trying to build is called *Word Up!*, and it is best described as a cross between Scrabble, Solitaire, and the Hunger Games in Space.

#### Demo

First things first: [Click here for a demo of what you are trying to accomplish][demo].

[demo]: http://htmlpreview.github.io/?https://github.com/jesseilev/word-up/blob/demo/index.html


Take note the following:

#### Rules of the Game

- The object of the game is to spell as many words as possible before time runs out, using only the letters specified.
- A word is invalid if it contains any letters that aren't in the specified set of allowed letters.
- A word is also invalid if it turns out not to be a real word.
- Your total score is the sum of the scores of all your valid words.
- The score of each word is the sum of the scores of each of its letters.
- The score of a letter is simply its score from the boardgame Scrabble.
- Unlike in Scrabble, you **may** use the same letter more than once in a single word.

#### The User Interface

- When the user clicks `New Game`, the letters are revealed and they can begin typing words.
- The letters are presented as little "chips" (I am going to refer to these things as chips throughout the assignment).
- Each letter chip contains a smaller chip indicating its points value.
- As the user types, the page provides continuous feedback. Specifically, if the word they are currently typing contains any letters that are not allowed, then the disallowed letters appear as red chips underneath the textbox.
- If the user tries to submit (presses Enter after typing) a word that contains disallowed letters, then the textbox simply clears and the word is not submitted.
- Once the user does submit a word containing only valid letters, it appears in a chip below the textbox.
- Shortly after a word chip appears, it will sprout a smaller (blue or red) chip indicating the points total for the word. A normal word will contain a blue chip with a number indicating its score. But a gibberish, nonexistent word will instead contain a red chip with an "X".
- Once the timer runs out, the textbox is no longer usable.

#### Room for Improvement

Note as well that there are some obvious places where the game could be improved, especially when it comes to the selection of the allowed letters:

- Sometimes none of your 7 letters are vowels, making it very hard to spell words!
- There is no special provision to make sure that if you receive a `q`, you also receive a `u`.
- Weird rare letters like `z` and `x` happen no less frequently than common letters like `e` and `t`.

Just wanted to point out that all these flaws are part of the assignment, and you are not required to fix them.

Of course, if you finish the normal assignment and want to improve the game, either by tweaking these imperfections or by adding cool new features, you are obviously encouraged to do so!

---
## The Pearson Dictionary API

Before diving into the code, let's take a second to get familiar with the API we'll be using.

What service do we need an API for? A dictionary. Our way of checking the validity of the user's word submissions will be to look up each word in the dictionary and see if it exists.

#### Pearson

[Pearson][pearson] is a textbook publish. But their [Dictionary API][pearson-api] is dead-simple to use. You don't even need to register for a developer key.

[pearson]: http://developer.pearson.com
[pearson-api]: http://developer.pearson.com/apis/dictionaries

Let's use Pearson's dictionary to search for the word "cheese": Open up a terminal make a `curl` request to this url:

```nohighlight
$ curl "http://api.pearson.com/v2/dictionaries/entries?headword=cheese"
```

You should shortly receive a fat wall of JSON about cheese.

As you can see, the main endpoint we want to hit is `http://api.pearson.com/v2/dictionaries/entries`, and we pass along an additional `headword` parameter with a value of `cheese`.

#### Specifying a Particular Dictionary

There is one more complication, which is that their default dictonary is very permissive. For example, pretty much any combination of two or three letters you can imagine will probably turn up a few results as an acronym for something. This is bad, because we don't want our game to reward players who simply hack away at random short combinations of letters.

Luckily, the API allows you to choose a more specific dictionary by changing the endpoint url to:

`http://api.pearson.com/v2/dictionaries/DICTIONARY_CODE/entries`

where you substitute a particular dictionary name in for `DICTIONARY_CODE`. See the [API page][pearson-api] for more details.

I have gotten pretty good results using the "Longman Active Study Dictionary", whose code name is `lasde`.

Great, you should now have all the tools you need to start looking up words in the dictionary! This will come in handy towards the end of the assignment.

---
## Obtaining the Starter Code

1. [Fork this repository][word-up-repo].
2. Clone your forked repo down to your local machine.

[word-up-repo]: https://github.com/bgschiller/word-up

---
## A Brief Tour of the Starter Code

Let's briefly look over the code you have inherited.

#### Preview in the Browser

Before looking at the code itself, you might want to quickly open up `index.html` in a browser window so you can see what the starter code *does*.

You can see the skeleton of the game, though nothing _does_ anything yet.

#### index.html

Now open up the source code in your text editor.

In `index.html`, note the following:

- We load our old friend, Vue.js in the `<head>`.
- The body of the document has a `<main>` element which is the mount-point for our Vue app. It is divided into two sections:
	- The `"pregame"` section, which contains elements that will be shown before the game starts. This section contains a scoreboard, and will soon contain a "New Game" button once you finish your first task.
	- The `"game"` section, which is initially hidden, and will only be revealed once the user clicks the "New Game" button. This section contains the form where the user types, and some containers that will be filled with chips (one for the letters, one for the submitted words).
- Inside the `"game"` section, you'll see what looks like a brand new html tag: `<letter-chip>`. This isn't truly an html tag; instead, it's a Vue component. Components are kind of like adding new tags to html that look and act the way we tell them to. It's kind of like how writing a function allows us to extend a programming language. We'll learn more about them soon.
- Towards the bottom of the body, you'll see a couple of `<script type="text/x-template">` elements. The `text/x-template` piece might be a clue: these pieces represent the _template_ for how we want our custom `<letter-chip>` and `<submitted-word>` components to look.
- Finally, we load our `scripts/wordup.js` file.

#### scripts/wordup.js

Turn your attention now to the `wordup.js` file.

This is a very large file, but you will definitely find it worth your while to spend 5-10 minutes looking it over and reading all the comments. I wrote those comments myself, and I *will* be offended if you don't read them 😉.

Broadly, the file is split up into a few sections:

- **Components**

	In this section we set up some "components" that we can use within our main Vue. These components are fairly simple, because they have no behavior&mdash;they don't <em>do</em> anything.

    Components will sometimes have `computed`, `methods`, `data`, or any of the other sections that we've seen in the main `Vue`. These ones only have two pieces though:

    - `template`: This defines how the component looks as html. The browser doesn't automatically know what a `<letter-chip>` should look like&mdash;we have to tell it! In this case, these are selectors telling Vue where in `index.html` it can find the template. It's also possible to put the template _right there_ as a string.
    - `props`: If components are like functions, props are like the arguments to functions. They're ways of changing or customizing how a component looks. For example, the `letter` prop in `<letter-chip>` tells the component which letter it should display.

- **Game Logic and Utils**

	These sections simply contain a bunch of helper functions relating specifically to the rules and logic of the game.

- **Main Vue**

    - `data`:

	The main function in this section is `render`. Render simply looks at the model, and re-draws everything it might need to draw, based on what the model looks like. Whenever the model changes, we will call `render` again to make sure the view is up to date. We used this same pattern in the FlickList project.

	This sections also contains a few helper functions to draw specialized parts of the view.

- **DOM Event Handlers**

	This section is pretty small. It just registers some callback functions as handlers for a few DOM events, such as when the user clicks the "New Game" button, or submits the form.

#### css/styles.css

Finally, take a look at `styles.css`. There are no TODOs on this file, but in order to do some of your Javascript code, you are going to need to be familar with some of the CSS classes already defined for us.

---
## Your Tasks

Time to get started!

I have bad news and good news for you. The bad news is that you have a lot (17!) of `TODO`s. The good news is that each task is relatively small, often only one or two lines of code, and you will be given fairly detailed guidance.

<img src="http://66.media.tumblr.com/2e96a51d21f3fa17d94af64c8cea61bd/tumblr_ndwyr0McLD1thj99uo4_250.gif" />

Your tasks are as follows:

#### 1. New Game Button

Add a "New Game" button in `index.html`.

- It will need an `@click` annotation. Which method should it call?
- If you give it the correct CSS classes, it will magically look nice.

*Confirmation:*

 - Clicking should cause the textbox to appear.

#### 2. Time Remaining

In the pregame section of `index.html`, make the time remaining update with the correct value.

- For reference, we do something fairly similar a couple lines below, to set the current score.

*Confirmation:*

- You should see that the time appears on initial page load.
- Even better, you should also see that the time starts to count down when New Game button is clicked! The reason this works is that, each second, the `startTimer` function is updating `data`, and Vue keeps `data` in sync with our html template.

#### 3. Focus the Textbox

Another thing that should happen, just to make the user experience a little better, is that the textbox should automatically receive "focus", so that the user can start typing immediately without having to physically click on it. See if you can find an example of this by googling "html input autofocus".

- Add the `autofocus` attribute to your `<input type="text"/>`.

*Confirmation:*

- As soon as the textbox appears, it should already have focus.

#### 4. Instructions for the User

In `index.html`, add some instructions above the textbox so the user knows what to do, e.g.:

> Spell as many words as you can, using only these letters:

*Confirmation:*

- You should see your instructions on the page.
- It will obviously look a little weird, because "what letters?"

#### 5. Letters Container

In `index.html`, create a `<letter-chip>` component for each letter in `allowedLetters`.

- Use a `v-for` to create several `<letter-chip>`s.
- pass in the `:letter` and `:value` props
- You can compute the value using the `letterScore` method.

*Confirmation:*

- Should magically fill up with letter chips now.
- Notice if you click New Game again, the letters change!

Now would probably be a good time to show your page to a friend and brag, "Check it out, I'm practically done with this assignment." If only you knew what's in store...

#### 6. Handle Input Event

The next handful of tasks will tackle that cool feature where we give immediate feedback as the user types. Specifically, we want to provide feedback to inform the user whenever the word they are typing contains any disallowed letters.

- Use Vue's `v-model` attribute to keep the textbox in sync with the `currentAttempt` data value

*Confirmation:*

- If you open up the console and type `app.currentAttempt`, you should now see that it always matches the text value that you have typed into the textbox.
- Additionally, you can even run `app.currentAttempt = 'tomato'` in the console, and the textbox will update to contain that value.


#### 7. Implement the `isDisallowedLetter` function.

Now let's make some visible indication appear. Notice the computed property in `wordup.js` called `containsOnlyAllowedLetters`. This code is attempting to check whether the user's current attempt contains any disallowed letters. It relies on another computed property called `disallowedLettersInWord`, which in turn makes use of a method called `isDisallowedLetter`, which is incomplete! Your job is to implement this function so that given any letter, it returns a boolean indicating whether or not the letter is "disallowed" by the current model.

- You can use the Javascript `includes` function as a way to check whether a particular thing is a member of a list.
- You might find it helpful to test the function in isolation by invoking it from the console, e.g. type `app.isDisallowedLetter("z")`, etc.

*Confirmation:*

- You should see that the textbox's text turns red whenever you type a disallowed letter.
- You should also be able to check `app.isDisallowedLetter("w")` in the JS console.

### 8. Red Letter Chips

We don't just want the text to turn red, we also want to inform the user about specifically *which* letters are not allowed. We do this by appending little red chips underneath the textbox, one for each disallowed letter.

We have a container already: `<div class="disallowed-letters">` to hold this little chips. There are styles to turn any `<span>` inside this div to look right. Use a `v-for` to make a `<span>` for each disallowed letter.

*Confirmation:*

- You should see the chips!

### 9. Game Over

Changing gears now, when time runs out and the game is over, we don't want the user to be able to continue playing the current game. The textbox should become disabled when the game ends.

- There is an HTML attribute called `"disabled"`. We can use `v-bind` syntax to set it according to a data value.
- Use `v-bind` (or the `:` shorthand) to disable the input unless a game is in progress. Is there a data value or computed property we can use to check if a game is in progress?
- A neat trick you can use to test your code without having to wait 60 seconds for the timer to run out is to open up the console and manually change the model's `.secondsRemaining` property to something low, e.g. `app.secondsRemaining = 2;`.

*Confirmation:*

- The textbox should lose its focus and no longer be usable once the timer runs out.
- You might also notice that if there's text in the box when the timer runs out, it's frozen there. That's not ideal, but we won't get around to fixing it in these instructions. See if you can tackle it if you're interested.

#### 10. Submit word on enter

When the user presses the enter key, we want to submit the `currentAttempt`. We'll use the `@keyup.enter` event attribute to call our `addNewWordSubmission` method.

- Add the event handler, being sure to pass along the word as a parameter.
- In the `addNewWordSubmission`, clear out the value of the text input once you're done with it.

*Confirmation:*

- If you type a word with only allowed letters and hit Enter, you'll be able to see it in the `app.wordSubmissions` list via the JS console.
- If you type a word that contains disallowed letters and hit Enter, the form will clear away, but the new word will not be added.


#### 11. Word Submission Chips

In the `#word-submissions` div, add `<submitted-word>`s to the DOM.

- You can do something very similar to what we did for the letter chips.
- Make sure to pass in props for `:word`, `:score`, `:loading`, and `:is-real-word`.
- You can use the `wordScore` method to fill in the `:score` prop.

*Confirmation:*

- You should now see the word show up when you submit the form.

#### 12. Pearson URL

In the `checkIfWordIsReal` function, provide the correct URL for the `fetch` call for the particular word that was passed in.

*Confirmation:*

- When you submit a word, you should hopefully see this appear on the console:

	> We received a response from Pearson!


#### 13. Is it a Real Word?

Now that we got a response, we need to use that response to answer the question: Is this word legit?

In the same `then` callback of the `fetch` call within the `checkIfWordIsReal` function, we have made a variable called `isARealWord`, and have assigned it a hardcoded value of `true`. Replace the hardcoded value with an actual answer.

Use the following (imperfect) hueristic to decide whether or not we have a "real word" on our hands: The `response` object contains a bunch of properties, one of which is a list of "matching entries" called `results`. If the `results` list is empty, then the word is not real. Otherwise, it is real.

It may be helpful to add a `debugger` statement to the callback, so you can inspect the `resp` variable. It may also be enough to look at what's printed out on the console.

*Confirmation:*

- Nothing visible. You should add your own `console.log` statement to check that this is working properly.

#### 14. Update `.isRealWord` of the Word Submission

Now that you know the correct answer, there is one more thing to do. You must find the appropriate item in `this.wordSubmissions`, and set its `.isRealWord` property accordingly.

<img src="https://media.giphy.com/media/3o7TKw7vcnyQa0Hldu/giphy.gif" style="width: 300px"/>

Let's back up a sec. (This will be a long digression, so get comfortable.)

You might have noticed, if you poked around on the console, that the `app.wordSubmissions` property is kind of weird. It turns out that the concept of a "word submission" is too complicated to be represented by a string alone. For each word, we need to keep track of several pieces of information: the string itself, its score, whether we've heard back from the Pearson API and, if so, whether or not the string is a real word (rather than just gibberish). So for each item in the `app.wordSubmissions` list, we actually want an *object* composed of four properties:

1. `word`, a string with the actual word typed by the user
2. `loading`, a boolean representing whether or not we've heard back from the Pearson API.
3. `isRealWord`, a boolean which is not added until we hear back from the API.

For example, suppose the user is in the middle of a game, and has previously typed two words: `"honk"`, and `"honq"`. While "honk" is a real word, "honq" is not. And so in this situation, our model should look something like this:

```js
{
    ...
    gameHasStarted: true,
    secondsRemaining: 42,
    wordSubmissions: [
        { word: "honk", isRealWord: true, loading: false },
        { word: "honq", isRealWord: false, loading: false }
    ],
    ...
}
```

Makes sense so far? Good, because it's about to get weirder.

The situation is further muddied by the fact that for each word submission, there is a brief period of time during which we *don't yet know* whether or not its string is a real word, because we are still waiting for a response from the dictionary API.

Suppose the user now submits another word, `"chunk"`. We need to add that to our `.wordSubmissions` list, but we do not immediately know whether or not "chunk" is a real word. You and I happen to know that "chunk" is real, but our program is dumb and must defer to the dictionary. So our program makes an AJAX call to the Pearson API. But remember that an AJAX call takes a few seconds to come back with a response, and in the meantime, we still don't have the answer. So during the brief period of time before the response comes back, we want our `app.wordSubmissions` to look like this:

```js
[
    { word: "honk", isRealWord: true, loading: false },
    { word: "honq", isRealWord: false, loading: false },
    { word: "chunk", loading: true }
]
```

Until we get the response back, the "chunk" object has a `loading` value of `true`, and `isRealWord` is `null`.

As soon as we *do* determine the answer, we can update the model, so that the list becomes:

```js
[
    { word: "honk", isRealWord: true, loading: false },
    { word: "honq", isRealWord: false, loading: false },
    { word: "chunk", isRealWord: true, loading: false }
]
```

That is how we want our program to behave. Each word submission object should contain a `.word` property, and *eventually* should also contain a `.isRealWord` property, after a brief delay. The first part is already done for you (go look at the `addNewWordSubmission` function again to see the code). But the second part is your job: you must add a `.isRealWord` property to the objects that don't already have them.

Let's finally turn to the task at hand. You are inside the `success` callback of the AJAX call to Pearson. You have just received the response for some particular word (let's continue pretending it is `"chunk"`), and you even know the answer now (either `true` or `false`), assuming you did the previous TODO. Your current `model.wordSubmissions` is a list of objects, most of which contain two properties, but at least one (the one we care about, whose `.word` property is `"chunk"`) does not yet contain a `.isRealWord` property. Your job is to find that list entry, and set its `.isRealWord` property to the correct answer (in this case, `true`).

In coding terms, you simply need to iterate over the list of submissions, and for each submission, check if its `.word` property is equal to the string in question. If so, assign the correct value to its `.isRealWord` property. Also, set its `.loading` property to `false`.

*Confirmation:*

- As the user, submit a few words (some real words and some gibberish). Next, after waiting a second, open up the console and type `"app.wordSubmissions"`, and you should see an accurate answer for each item's `.isRealWord` property.


#### 15. Finish Implementing the `wordScore` Function.

Now let's fix those zeros and get the real score showing up next to each word. The problem is that the `wordScore` function is incomplete.

- You have a list of letters in a variable called `letters`. You must map that list of letters into a list of scores, one for each letter, and assign that list into the new variable, `wordScores`.

*Confirmation:*

- You should see a correct score next to each submitted word.

#### 16. Finish Implementing the `currentScore` Function.

This is a rewarding one. You probably noticed that the scoreboard always says 0, no matter what words have been submitted. That's because the `currentScore` function is incomplete!

Notice that it always returns a hardcoded value of `0`. Replace that `0` with the real answer, which is the sum total of all the word scores.

- Notice that you have a list of word scores available to you. You simply have to add those numbers up and return the total.

*Confirmation:*

- You should see real scores on the scoreboard!

#### 17. Finish Implementing the `addNewWordSubmission` Function.

Just one last loose-end to tie up! Currently the user is able to cheat by submitting the same word again and again. Let's fix the `addNewWordSubmission` function so that repeats are rejected.

- The variable `alreadyUsed` is currently hardcoded to `false`. But if the user has already used the word in question, then that value should be `true`. Determine the actual answer.

*Confirmation:*

- If you try to submit the same word more than once, the textbox should simply clear away your text and no new word submission will be added.
