import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import numpy.random as rd
import seaborn as sns

st.title('Void Aura Estimator')
st.markdown('### An AdventureQuest Worlds Guide')

st.markdown("This dashboard shows the data visualisation for the expected number of days required to obtain **7480** Void Auras for the Necrotic Sword of Doom in AdventureQuest Worlds, using the quests **_'Retrieve Void Auras'_**, **_'Gathering Unstable Essences'_**, or **_'Commanding Shadow Essences'_**, and based on the user's following inputs:")
st.markdown('- Current number of Void Auras')
st.markdown('- Number of Quests to be completed per day')
st.markdown("- Whether the Daily Quest **_'The Encroaching Shadows (Daily)'_** or **_'Glimpse Into The Dark (Daily)'_** is completed every day")

st.markdown("""---""")

st.markdown('### User Inputs:')
st.markdown('\n')



# Code to read user's inputs

current = st.number_input('Choose the amount of Void Auras you currently have:', min_value = 0, max_value = 7479, 
                    value = 500, step = 1)

quests_per_day = st.number_input("Enter the number of times you aim to complete the quest 'Retrieve Void Auras', 'Gathering Unstable Essences', or 'Commanding Shadow Essences' per day:", min_value = 1, max_value = 500, value = 5, step = 1)

dq_options = ['The Encroaching Shadows (Daily) - [Non-Member]', 'Glimpse Into The Dark (Daily) - [Member Only]', 'Both Daily Quests', 'None']

dq_choice = st.selectbox('Which Daily Quest do you plan to do every day?', dq_options)



# Define a function to return the mean number of Void Auras from a sample of n, depending on whether there is a Void Aura boost

def mean_aura(n, boost_status):

    aura_list = []
    if boost_status == True:
        for i in range(0, n):
            x = np.random.choice(np.array([5, 10, 20]), p = [1/3, 1/3, 1/3])
            aura_list.append(x)

    elif boost_status == False:
        for i in range(0, n):
            x = np.random.choice(np.array([5, 6, 7]), p = [1/3, 1/3, 1/3])
            aura_list.append(x)

    return np.mean(aura_list)

amt_req = 7480
amt_farm = amt_req - current

st.markdown('There are **{}** Void Auras left to obtain before reaching the target of **7480** Void Auras.'.format(int(amt_farm)))



# Simulation of a 1000 times to find the mean return of auras out of a sample size of n = 100 tries

x_ord = np.array([mean_aura(100, False) for i in range(0, 1000)])
y_ord = np.ceil(amt_farm / x_ord)

x_boost = np.array([mean_aura(100, True) for i in range(0, 1000)])
y_boost = np.ceil(amt_farm / x_boost)



# Obtaining values used for the KDE Plots

if dq_choice == dq_options[0]:
    exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 50)
    exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 50)
    
elif dq_choice == dq_options[1]:
    exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 100)
    exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 100)

elif dq_choice == dq_options[2]:
    exp_days_ord = amt_farm / ((quests_per_day *  x_ord) + 150)
    exp_days_boost = amt_farm / ((quests_per_day * x_boost) + 150)

elif dq_choice == dq_options[3]:
    exp_days_ord = amt_farm / (quests_per_day *  x_ord)
    exp_days_boost = amt_farm / (quests_per_day * x_boost)
    
st.markdown('### Data Visualisation')



# Plotting the 2 graphs: With and without Void Aura Boosts

plt.style.use('seaborn-whitegrid')
fig, ax = plt.subplots(figsize = (12, 10), dpi = 300)

ax = sns.kdeplot(data = exp_days_ord, label = 'Without Void Aura Boost', color = 'red')
ax2 = sns.kdeplot(data = exp_days_boost, label = 'With Void Aura Boost', color = 'blue')

plt.title('Expected number of days to reach 7480 Void Auras based on User Input', fontsize = 18)
plt.xlabel('Estimated number of days to reach goal', fontsize = 15, labelpad = 10)
plt.ylabel('Probability Density Function (PDF)', fontsize = 15, labelpad = 10) 



# Obtain x and y values of maximum points to plot the expected number of days

data_x, data_y = ax.lines[0].get_data()
xi = np.median(exp_days_ord)
yi = np.interp(xi, data_x, data_y)
plt.plot(xi, yi, marker = 'o', color = 'black')

data_x2, data_y2 = ax2.lines[1].get_data()
xi2 = np.median(exp_days_boost)
yi2 = np.interp(xi2, data_x2, data_y2)
plt.plot(xi2, yi2, marker = 'o', color = 'black')




# Labelling maximum points

plt.text(xi, yi, '~ {} day(s)'.format(int(np.ceil(xi))), fontsize = 15, color = 'r', ha = 'left', va = 'bottom')
plt.text(xi2, yi2, '~ {} day(s)'.format(int(np.ceil(xi2))), fontsize = 15, color = 'b', ha = 'left', va = 'bottom')




# Adjusting Plot Legend

legend = plt.legend(loc = 'upper left', frameon = 1, framealpha = 1, fontsize = 15)
frame = legend.get_frame()
frame.set_facecolor('lightcyan')
frame.set_edgecolor('black')

st.pyplot(fig)



# Statistical Summary
st.markdown('## Statistical Summary')
st.markdown('#### Without Void Aura Boost')
st.markdown('Expected Number of Days: **{}**'.format(int(np.ceil(xi))))
st.markdown('Standard Deviation: **{}**'.format(round(np.std(exp_days_ord), 3)))

st.markdown('#### With Void Aura Boost')
st.markdown('Expected Number of Days: **{}**'.format(int(np.ceil(xi2))))
st.markdown('Standard Deviation: **{}**'.format(round(np.std(exp_days_boost), 3)))

dif = int(np.ceil(xi)) - int(np.ceil(xi2))

st.markdown('#### Time saved by obtaining Void Auras during a boost')
st.markdown('Number of days saved: {}'.format(dif))
st.markdown('Time spent farming reduced by **{}%**'.format(round(dif/int(np.ceil(xi))*100, 2)))

st.markdown("""---""")
