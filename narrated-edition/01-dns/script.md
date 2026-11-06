# DNS: How a Website Name Finds Its Address

## 01. A photo lives somewhere

You type a website name, and a photo appears. But where did that photo come from? Let's slow that tiny moment down. Your computer does not already have the photo. Another computer stores it and can send it back. A computer doing that job is called a server. The line between them represents a way to exchange messages. But there are countless possible destinations. Before asking for the photo, your computer needs to know which address to contact. How does it find that?

## 02. Names are easier to remember

Think about calling a friend. You remember their name; your phone uses a number. Websites have a similar split. We type a name, while the network uses a number called an IP address to help deliver messages. Watch the name turn into an address. DNS, short for Domain Name System, helps make that lookup. Our pretend website is photos.orbit.example. The address is made up for teaching too. You don't need to memorize either one.

## 03. Ask a helper

Your computer could ask, where is this website? But who should answer? Meet one helper, shown in green. Its job is to find the address and bring it back. The technical name for this helper is a resolver. That's all the word means here: it resolves our question. Start with just these two characters, your computer and its helper. Assume the helper hasn't saved an answer yet. We are going to follow its search together.

## 04. A name has smaller parts

A single helper cannot keep a fresh list of every website. Instead, responsibility is split into smaller parts. Look at the dots in photos.orbit.example. Read from the right: example, then orbit.example, then the full name. It's like opening a large folder, then a smaller folder inside it. This nested arrangement is called a hierarchy. The dots tell the helper how to narrow its search. No address yet; first we are learning where to ask.

## 05. Start at the directory

The helper begins at a starting directory called the root. Imagine a reception desk that says, for names ending in example, ask over there. It gives a useful direction, not the website's final address. That direction is called a referral. Follow the question going out and the clue coming back. The helper now knows its next stop. In this drawing, each circle is a job performed by DNS servers, not one unique machine for the whole world.

## 06. Follow one useful clue

The next directory handles the last part of our name: example. That part is called a top-level domain, or TLD. You have seen real ones such as com and org. Our teaching name uses example. This directory points toward the people responsible for orbit.example. Notice the pattern: ask a broad directory, receive a narrower direction, ask again. The helper is doing this work for us. Your browser doesn't need you to visit these directories yourself.

## 07. Find the address keeper

Now we reach the keeper of the website's DNS information. This is called an authoritative server because it holds the relevant official record. In our example, that record pairs the photo website's name with 192.0.2.10. Finally, a number! The earlier stops were useful even though they didn't know it. They guided our helper here. Watch the green answer travel back. We found the address by following responsibility from a broad directory to a specific record.

## 08. Bring the answer home

The helper gives that address to your computer. Now your computer can try to contact the photo server. The name lookup has finished; asking for the actual photo is a separate step. Think of finding a friend's phone number: you still have to make the call. DNS hasn't delivered the picture itself, and an address doesn't promise the server will answer. It has solved one smaller problem: turning the name you recognize into useful contact information.

## 09. Put a clock on it

How long did that search take? A millisecond is one thousandth of a second. Let's give our example four small waits: two milliseconds for the helper exchange, then twenty, thirty, and forty for its three directory exchanges. Watch each colored piece extend the time bar. Add them: two plus twenty plus thirty plus forty makes ninety-two milliseconds. These are chosen numbers, not promised Internet timings. We add because each step needs the previous step's answer.

## 10. Remember the answer

What happens when someone asks the same question again? The helper can keep a temporary copy of the answer. That saved copy is called a cache. Now the long trip disappears: in our example the reply needs only two milliseconds. Ninety-two divided by two is forty-six, so this lookup is forty-six times quicker. Only the lookup! We haven't made the photo download forty-six times faster. Saving a useful answer simply avoids repeating work we already did.

## 11. Memory needs an expiry date

But websites can move. If our helper remembers an address forever, it might keep sending people to an old place. So the saved answer comes with a time limit. Here it is sixty seconds. Its name is time to live, or TTL. Watch the timer count down. Reading the saved answer does not restart that timer. Think of a note with an expiry time printed on it: using the note doesn't make the information new again.

## 12. What if the address changes?

Let's move the website while the timer still has thirty seconds left. The official record changes to a new address, 203.0.113.20. Does our helper magically know? No. It still has the old saved copy and may reply with that address until its allowed time runs out. The two boxes now show different numbers. This explains why changing a website's DNS record can take time to be noticed everywhere. Copies don't all update at the same instant.

## 13. Look again when time runs out

The countdown reaches zero. For this example, the next request makes the helper look again. This time it finds the new address and replaces its old copy. We show the directory trip again so the refresh is easy to follow; real helpers may remember some directions and skip steps. Our useful rule is simple: reuse an answer for a while, then check again. A temporary memory gives us speed without pretending that yesterday's information must stay true forever.

## 14. Connected, but missing directions

Now we can try a little mystery. Leave the network connection working, but stop our helper from finding the address. An app may fail before it knows where to send its request. Meanwhile, another task that already knows its destination can keep going. So online does not always mean every website name can be found. We have broken only the naming step in this experiment. Real failures can have other causes, but this picture explains one possible reason.

## 15. Three jobs, one simple search

Let's shrink the whole journey into three pictures. First, split the directory into smaller branches. Second, follow directions until the right record answers. Third, remember that answer briefly. The formal words are hierarchy, referrals, and caching. You already know what those words describe because you've watched them happen. The countdown adds one more detail: remembered answers need a time limit. These jobs work together so no single directory has to hold every fresh answer to every question.

## 16. From a name to an address

Return to the photo. A name you can remember becomes an address the network can use. A helper finds it, directories guide the helper, and temporary memory saves repeat trips. That's the core of DNS. Next time you type a website name, imagine that small search taking place before the page begins to arrive. It may finish almost instantly because somebody remembered the answer. The website name looked like a destination; first, it was a question.
