**Coding Task: Chat and Ad Generation**

This task is a follow-up from the previous high-level design task. We’ll focus on several aspects of ad generation, specifically on the construction of the ad storyboard and fitting of media elements (i.e., assets) into templates. Due to time constraints, it's likely you won’t be able to finish all sections. Please follow this order of priority and skip sections of lower priority—emphasizing depth over breadth in your approach:

1. **A: Ad Storyboard Design Agent (Main Task)**
2. **C: Video Cutdown Generation (Main Task)**
3. **C: Video Cutdown Generation (Follow-up/Advanced/Further Discussion)**
4. **A: Ad Storyboard Design Agent (Follow-up/Advanced/Further Discussion)**
5. **B: Asset & Template Fitting Process**

### **A: Ad Storyboard Design Agent**

You are tasked with creating a chatbot that gathers basic information about an ad and follows up with more specific questions, guiding the user through the ad generation process. The steps proceed as follows:

1. **Welcome Message:** “What would you like to do today?”

2. **User replies:** “Make me an ad” → This triggers a routine (via Agents or other methods) to gather basic information:

   a. Ad Duration (in seconds, ranging from 0 (for static ads) to ~60s)  
   b. Ad Channel (e.g., Facebook, Instagram, TikTok, etc.)  
   c. Ad Theme (a short ~50-word description of what the ad should be about)  

   The user may provide all or partial information, and the chatbot should prompt for any missing inputs.

3. Once Step 2 is complete, trigger an LLM prompt completion (based on a well-crafted system prompt describing the LLM’s role as an ad writer, supplemented by user inputs) to generate a brief ad concept (~100 words elaborating on the provided theme).  

   a. Additional input: The client’s brand description (a ~200-word paragraph describing the brand’s value proposition and style) will be retrieved from a simple database lookup.  

   **Example Input & Output:**

   **System Prompt:**  
   "You are an expert ad creative agent tasked with writing high-level ad story concepts. You are given information about the client’s brand description and ad theme..."

   **User Input:**  
   Ad Theme: <e.g., "ice cream in winter">  
   Brand Description: <Database lookup result for the current user/client>

   **Output Ad Concept:**  
   <e.g., "Enjoy the delight of delicious ice cream in a winter wonderland...">

4. After Step 3, the user will be presented with the generated Ad Concept. The user should be prompted to either validate it or ask the chatbot to rewrite the concept. They may or may not provide feedback or specific direction for revision.

5. After the user confirms the Ad Concept, proceed to generate a scene-wise storyboard. Use the Ad Duration input to determine the number of scenes:  
   0s = 1 scene (static ad),  
   <10s = 3 scenes,  
   <30s = 5 scenes,  
   <60s = 7 scenes.  

   This will trigger another LLM call to generate the scene-wise storyboard. Each scene should flow from one to the next, forming a coherent narrative (beginning, middle, and end).

6. The user is again asked for confirmation on whether they like the ad storyboard. They may request alterations (e.g., “change Scene 1” or “add 1 more scene”). Once the user is satisfied with the final output, prompt them for final confirmation, and if they reply “Yes,” proceed with asset and template fitting.

**Design a chatbot system to handle Steps 1 through 6, following this priority:**

1. Prioritize designing the “happy flow” where the user replies “OK” to validation in Steps 4 and 6.  
2. Implement form validation in Step 2 if the user doesn't provide all the necessary information.  
3. If time permits, implement a flow for regenerating the Ad Concept in Step 4 when the user provides negative feedback (with or without specific guidance).  
4. If more time is available, design a flow for handling back-and-forth chat-based editing in Step 6, where the user might even backtrack to Step 1 (e.g., “I don’t like any of this, let’s change the Ad Theme”).

### **B: Asset & Template Fitting Process**

This task follows from Task A’s output. Assume we have a set of templates, each containing multiple scenes. Each scene is a pre-designed visual with placeholders for images, videos, and text assets. An ad is composed of a sequence of scenes, transitioning smoothly between them via pre-designed animations (these can also apply to individual asset placeholders).

**Example Template with Placeholders:**

Let’s focus on the case where we have a template of N scenes, each containing a mix of video and image placeholders. The goal is to fit the right video clips, images, and text into the placeholders.

**Steps:**

1. Given the user’s brand description and storyboard requirements, and using a fixed template, generate an advertisement storyboard (a short paragraph for each scene describing its theme). Ensure the storyboard for each scene flows as a narrative.  

   **Example Storyboard:**

   Scene 1: Winter Indulgence  
   Scene 2: Warmth and Comfort  
   Scene 3: More is More  

2. Based on the storyboard, generate text slogans that are semantically relevant to each scene.  
3. Select (or generate) images and video clips that semantically match the storyboard for each scene, ensuring consistency in visual and textual elements.

Propose a more detailed design solution for this task, including pseudocode or flow diagrams. If possible, provide prompt examples or a working demo.

### **C: Video Cutdown Generation**

For video cutdowns, the traditional method involves detecting frame changes (e.g., using HSV or similar methods). In ads, we need to piece together these segments to fit them into a video ad of a specific duration (e.g., 20s).

**Steps:**

1. Write a simple set of classes to represent a video and its constituent clips:

   - Each clip has an original Video ID  
   - Each clip has a start and end timestamp  
   - Optionally, each clip may have a “scene change threshold” (visual change between clips)  
   - Optionally, clips may have text descriptions or contextual embeddings.

2. Write an algorithm to pick a subset of video clips that sum up to the required ad duration. For instance, to generate a 15s cutdown from a 1-minute video, choose segments such as {3s, 4s, 6s}, summing to ~13s.

**Additional Considerations:**

1. Allow the user to specify semantics for cutdowns (e.g., “give me a 10s cutdown of people walking in the city”).  
2. Handle N x M matching, where you pick the best M video clips that match N storyboards.

