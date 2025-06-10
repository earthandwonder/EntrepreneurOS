# App Ideas Viewer

A Python GUI application for easily browsing and searching through your app ideas stored in JSON format.

## Features

- **Clean Interface**: Two-panel layout with ideas list on the left and detailed view on the right
- **Search Functionality**: Real-time search across all fields (name, keywords, functionality, etc.)
- **Easy Navigation**: Click on any idea in the list or use Previous/Next buttons
- **Automatic Loading**: Automatically loads `LLM_Friendly_App_Ideas.json` if present in the same directory
- **Formatted Display**: Color-coded fields with proper formatting for easy reading

## Requirements

- Python 3.x (tkinter is included with most Python installations)
- No additional dependencies required

## Usage

### Quick Start
1. Make sure your `LLM_Friendly_App_Ideas.json` file is in the same directory as the script
2. Run the application:
   ```bash
   python app_ideas_viewer.py
   ```

### Manual File Loading
1. Run the application:
   ```bash
   python app_ideas_viewer.py
   ```
2. Click "Load JSON File" button to select your JSON file

### Navigation
- **Click on any idea** in the left panel to view its details
- Use **Previous/Next** buttons to navigate sequentially
- The **counter** shows your current position (e.g., "5 / 59")

### Search
- Type in the **search box** to filter ideas in real-time
- Search works across: Name, Keywords, Functionality, Marketing, Skills to Learn, and Tech Stack
- Click **Clear** to remove search filter and show all ideas

## Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│ [Load JSON File] Loaded: filename.json (59 ideas)          │
├─────────────────────────────────────────────────────────────┤
│ Search: [________________] [Clear]                          │
├──────────────────────────┬──────────────────────────────────┤
│ Ideas List:              │ [Previous] [Next]     5 / 59    │
│ ┌──────────────────────┐ │ ┌────────────────────────────────┤
│ │ 1. Coin Toss         │ │ │ 5. Love quotes                 │
│ │ 2. Checklist         │ │ │                                │
│ │ 3. Quotes by Naval   │ │ │ Origin: Brainstorm             │
│ │ 4. Color picker      │ │ │                                │
│ │ ▶ 5. Love quotes     │ │ │ Keywords: love quotes [25,60]  │
│ │ 6. Aboriginal seasons│ │ │                                │
│ │ ...                  │ │ │ Functionality: Displays        │
│ └──────────────────────┘ │ │ curated love quotes to inspire │
│                          │ │ users daily.                   │
│                          │ │                                │
│                          │ │ Skills to Learn: Daily         │
│                          │ │ notifications; Favorites and   │
│                          │ │ sharing options                │
│                          │ └────────────────────────────────│
└──────────────────────────┴──────────────────────────────────┘
```

## Tips

- The application remembers your position when searching, so you can explore filtered results easily
- Only fields with content are displayed to keep the interface clean
- The search is case-insensitive and matches partial words
- Ideas without an Order number will appear at the bottom of the list 