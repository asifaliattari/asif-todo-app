# ✅ Manual Testing Checklist

## Quick Test - Do This Now! (5 minutes)

### Test 1: Create Account ✅
1. Open: https://asif-todo-app.vercel.app/signup
2. Fill in:
   - Name: Your Name
   - Email: yourtest@email.com
   - Password: TestPass123!
   - Confirm Password: TestPass123!
3. Click "Create Account"

**Expected Result:**
- ✅ Redirects to tasks page (/)
- ✅ Shows empty task list
- ✅ Shows "Add Task" button

**If you see this = DATABASE IS WORKING! 🎉**

**If you get an error:**
- Note the error message
- Check browser console (F12 → Console tab)
- Share the error with me

---

### Test 2: Create Tasks ✅
Once logged in:
1. Click "Add Task" or "+" button
2. Enter:
   - Title: "Complete hackathon project"
   - Description: "Finish Phase II deployment"
3. Click "Save" or "Create"

**Expected Result:**
- ✅ Task appears in the list
- ✅ Shows creation time
- ✅ Has checkbox (unchecked)

Repeat 3-4 times with different tasks.

---

### Test 3: Mark Task Complete ✅
1. Click checkbox next to a task
2. Observe the change

**Expected Result:**
- ✅ Task marked as complete (checkmark appears)
- ✅ Task might move to "Completed" section
- ✅ May show strikethrough styling

---

### Test 4: Update Task ✅
1. Click on a task title or "Edit" button
2. Change the title or description
3. Save changes

**Expected Result:**
- ✅ Task updates immediately
- ✅ Changes are saved
- ✅ No page reload needed

---

### Test 5: Delete Task ✅
1. Find delete button (trash icon) on a task
2. Click it
3. Confirm if prompted

**Expected Result:**
- ✅ Task disappears from list
- ✅ No error message

---

### Test 6: Data Persistence ✅
1. Refresh the page (F5)
2. Check if tasks are still there

**Expected Result:**
- ✅ All tasks remain
- ✅ Completed status preserved

---

### Test 7: Logout & Login ✅
1. Click "Logout" button
2. Should redirect to login page
3. Login with same credentials
4. Check tasks

**Expected Result:**
- ✅ Successfully logs out
- ✅ Can log back in
- ✅ All tasks still visible
- ✅ Data persisted in database

---

### Test 8: User Isolation ✅
1. Logout
2. Create a NEW account (different email)
3. Check if you see any tasks

**Expected Result:**
- ✅ Should see NO tasks (empty list)
- ✅ Previous user's tasks are NOT visible
- ✅ Each user has separate data

---

## Results Summary

After completing all tests, report:

| Test | Status | Notes |
|------|--------|-------|
| 1. Signup | ⏳ | |
| 2. Create Tasks | ⏳ | |
| 3. Mark Complete | ⏳ | |
| 4. Update Task | ⏳ | |
| 5. Delete Task | ⏳ | |
| 6. Data Persistence | ⏳ | |
| 7. Logout/Login | ⏳ | |
| 8. User Isolation | ⏳ | |

---

## If ALL Tests Pass: YOU'RE DONE! 🎉

Next steps:
1. ✅ Record demo video (90 seconds)
2. ✅ Submit to hackathon
3. ✅ Celebrate! 🎊

---

## If Any Test Fails:

Let me know:
1. Which test failed
2. What error message you saw
3. What happened vs what was expected

I'll help you fix it immediately!
