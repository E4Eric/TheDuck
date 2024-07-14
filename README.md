![vd6(Small)](https://github.com/E4Eric/TheDuck/assets/2371669/7fc8409f-e41a-41b2-b3a1-10b412423489)



# The Versatile Duck

> **_"A UI is an attempt to allow the user to push their ideas through a keyboard and a mouse; good ones help with this"_** ;-)

The Duck is a UI Toolkit architecture that was designed using a first principals approach.
Let's imagine we exist at a time before UI Toolkits and we're trying to design one from scratch using
what we know now about the applications we need to support.

Over the years UI's have converged on a 'conventional' presentation for interacting with thr User. We all know them; Menus, Toolbars and such. This is by necessity once the user base expands to the general population (i.e. your grandma...;-) these folks need standard metaphors.
I'll refer to these as 'conventional' apps.

'Versatile' comes from the duck's being a 'pure' architecture, it only defines the concepts without inferring how they might be used.
As such it can mimic the UI of any app, from a simple calculator to a complex IDE. Importantly, the calculator doesn't need to bring any baggage that might be needed to support more complex spps.

What are the fewest number of concepts that can be used to build a UI Toolkit that can mimic 'conventional' UI Apps?

First let's identify the things we cannot possibly do without:
- We're an app in some language so we need a 'main'
- We're a UI app so we need a 'window' to draw on and to hook into mouse / kb events
- We need a model to contain the definition and meta-data need to define the application

Here 'main' does the normal things; arg parsing / verification... Then it loads the model and instantiates the 'window', passing in the modelas a constructor arg.

To ensure that  aren't making a toy we'll use one of the more complex UI's; the Eclipse IDE.
This has two advantages; it's a complex UI and it's open source so the Eclipse license allows me to use the icons etc without encountering potential IP issues.
I'm also thoroughly familiar with it having been a Platform UI committer for a=over a decade (and the dev lead for e4).

# Observations

There are a certain patterns we can observe in the UI's of the most popular apps
which can be used to inform the required architecture.

1. The UI is a tree of components. Each component has a parent and zero or more children.
2. The layout of these components completely tiles the app window (i.e. there are no 'holes'). The combination of these rwo means that we can use recursion for the three main support operations:

3. The file system is your friend. SSD's remove the latency issues which caused current caching strats, Now we can use the projects file structure directly.
1. Layout: The layout traverses the tree of UI elements asking the same question:
   1. How much space do you need? We call each element's layout code passing in the element to be drawn as well as the 'available' space.
   2. The layout code lays out the child elements (recursively) and ultimately returns the remaining available area. Important to note is that as each stage of the layout progresses it captures the final screen position in the associated element.
2. Drawing: The drawing code traverses the tree of UI elements asking the same question:
   1. Draw yourself.
   2. Draw your children Note that sice we've already cached the 'draw rect; we can call the 'render' method for the UI element passing in nothing except the UI element itself
3. Picking: Again we traverse the tree this rime asking whether the element lies under the cursor. Note that we can early prune the iteration; there is no point checking tke children of any element wjose parent is not under the cursor.

# The Answer

Ok, we're trying to mimic this:

[ Cap of Eclipse UI]

Notice that there is no mention of the usual UI Widgets (remember...they don't exist yet ;-).
In its pure form a UI presents the user visual cues that identify possible options for interaction.
What's interesting in the image above?
  
- There are a number of words arranged along the top
- Below are a bunch of images that appear to be grouped
- The main area is sub-divided into boxes, each having their own (similar) arrangements of words and images

At this point we're only trying to look like a duck; what do wee need to replicate this?

# The Core architecture
First we'll define the main components of the architecture and we'll add extras to support
behaviours (i.e. walk like a duck)
## Display Manager
The first requirement is to decide which low level window API we want to use. Note that this will likely also determine
which language we'll use to write the other components in 
## Model Manager 
 This manages model operation like Load / Save as well as the main iteration based operations; Layout, Draw and Pick  


- We need a model; for now it only has to define the UI as given in the screen cap

## The Model
We start with the model because *everything* starts with the model. IMO this should be true
of all applications, not just UI's. Programming was originally called 'information processing' for a reason.
At some point we lost track of this and focussed on algorithms instead...

Models that expect to be displayed / manipulated in a UI need a model that supports a proper update mechanismm out of the box.

It works like this:
- Start with a given model state being displayed
- Some action in the UI makes a *suggestion* to the model that it would like to change the model (add/remove of modify an element's field). NOTE: it must not pre-suppose that the change will occur
- The Model tests the validity of the change by querying a list of 'business rules'
  - If valid the new state is applied to the model
  - If not it takes whatever remedial by reflecting back to the rule that failed

My models have used the same design for over two decades a controllable 
- Structurally think JSON
- Model Element property values may be directly accessed (for performance) but may *only* be modified through an API provided by the Model Manager
- The ModelManager provides an event bus that allows participants to register a listener callback onto the bus
- The bus is global in the sense that all changes to a model element are reported so callbacks should bail as soon as they determine they

The modification proposed through the API call *is a suggestion*; callers of this API must ensure that they don't pre-suppose that the change will take place.
The manager then:
- Validates the suggestion and updates the model if it's valid
- If the proposal 

The Model Manager may choose to ignore or modify the suggestion if it violates the rules of the model (as defined as defined on a per-application basis 

We require a model that defines what the component tree looks like along with any necessary info needed for wither the layout or rendering steps

OK, here's where I cheat by using my knowledge of future UI architectures...;-)

Both the 'Main Menu' and the 'Toolbars' (as well as the buttons inside them) are horizontally 'Tiled'
The 'Part Stack' are defined by the amount of screen they take up





