image_prompt="""Identify the objects in the given image. Identify only the main objects in focus"""

text_prompt="""Identify objects or items in this text that can be donated. \n\n Text: {text} \n\n. Do not give a description. Just the objects that can be donated.Return the output in the format: [object1, object2, object3]"""

categorise_prompt="""
**Prompt:**

You are given a list of objects detected in an image and a set of NGOs, each with a list of items they require. Your task is to categorize the detected objects and match them with the NGOs that need them. The input will include the detected objects and the NGO data, structured as follows:

- **objects**: A list of detected items from the image.
- **NGO_DATA**: A dictionary where each key is an NGO name, and the corresponding value is a list of items that NGO requires.

You need to return a list of NGO names that accept at least one of the detected items.

---

### **Example Input:**

**objects:**  
```
item2, item5
```

**NGO_DATA:**


{{
  "NGO1_Name": ["item1", "item2", "item3"],
  "NGO2_Name": ["item4", "item2"],
  "NGO3_Name": ["item5"]
}}


### **Expected Output:**

```
[NGO1_Name, NGO2_Name, NGO3_Name]
```

---

### **Actual Input:**

**objects:**  
```
{objects}
```

**NGO_DATA:**

```
{NGO_DATA}
```

---

Based on this input, return a list of NGO names that match the detected objects. Do not return any other information, stick to the format provided in the example.
Do not change the NGO names in the input. Return the output as it is
---
"""
