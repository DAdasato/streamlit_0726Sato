import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title('1日の消費カロリーメーター')
st.write('一日の消費カロリーを知って、食事や運動に生かそう！')
st.write('※これはあくまでも目安です。これを指標として、日々の運動と食事を意識しましょう！')

def recommend_meal(calorie):
    if calorie < 1500:
        return "消費カロリーが低いため、バランスの取れた食事を心掛けよう。例えば、筑前煮など１食400kcal程度の食事がおすすめ!", "https://assets.st-note.com/production/uploads/images/28963188/picture_pc_e1df18e1d01c2ebfa4de4348ea92b9b5.jpg?width=800" 
    if 1500 <= calorie < 2000:
        return "消費カロリーに合わせて、野菜、たんぱく質、炭水化物をバランスよく摂取することが大切。例えば、鶏もも肉のソテーなどの１食600kcal程度の食事がおすすめ!", "https://www.marukome.co.jp/recipe/special/eiyoshi/img/menu/img_menu01.png?tm=1654071308"
    else:
        return "アスリート並みの消費カロリーのため、たんぱく質と炭水化物をしっかり取ろう。例えば、高カロリーの食事で、１食800kcal程度の食事がおすすめ！", "https://athtrition.com/wp/wp-content/uploads/2017/01/IMG_9944s.jpg"

def calculate_calorie(gender, age, weight, height, activity_level):
    if gender == "男性":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    if activity_level == 1:
        calorie = bmr * 1.2
    elif activity_level == 2:
        calorie = bmr * 1.375
    elif activity_level == 3:
        calorie = bmr * 1.55
    elif activity_level == 4:
        calorie = bmr * 1.725
    else:
        return "適切な選択肢を入力してください"

    return calorie

def display_overeating_tips():
    st.subheader("食べすぎた次の日の対処法")
    tips = [
        ("1. 低カロリーの食事を心がける", "https://nosh.jp/magazine/wp-content/uploads/2022/10/th_%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB-11-740x494.jpg.webp", "食べ過ぎた次の日は、食事を「軽め」にしましょう。つまり、カロリーを低めに抑えることで、食べ過ぎをリセットしましょう。1日に必要なエネルギー量は、活動量の少ない女性の場合で、1,400〜2,000kcal、男性ならば2,000〜2,400kcalです。あなたが女性で、仮に食べ過ぎた日に3,000kcalくらい摂ってしまったとします。それならば、翌日を1,200kcal、翌々日を1,400kcalというようにカロリーを控えるようにしましょう。このように食べ過ぎた次の日から数日間、カロリーをコントロールすれば、太る心配は少ないと言えます。"),
        ("2. 水分をしっかり摂ろう！白湯を飲むのもおすすめ", "https://nosh.jp/magazine/wp-content/uploads/2022/10/th_%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB-10-740x493.jpg.webp", "常温の水を飲めば、体が温まり、代謝が良くなります。つまり、水を飲むことで、筋肉へ十分な血液が送られます。すると、筋肉量が増え、基礎代謝量が上がるのです。よりしっかり体を温めたい場合は、白湯さゆを飲むのもおすすめです。さらに食事の際も意識して水分を摂れば、早食いになりにくくなります。ゆっくりと食べることで、満腹感も得やすくなります。その結果として、食べすぎを防ぐことができます。このように、水を飲むことには、ダイエットに関連する利点がたくさんあります。人の体は約60%が水分でできています。水分は食事からも摂取できますが、1日1.2L以上は水を飲むことを目標にして、積極的に水を飲みましょう。"),
        ("3. ウォーキングやストレッチでカロリーを消費しよう", "https://nosh.jp/magazine/wp-content/uploads/2022/10/th_%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB-9-740x492.jpg.webp", "ウォーキングやストレッチといった有酸素運動を取り入れ、エネルギー消費を増やしましょう。そうすることで、食べすぎのリセットに効果を発揮します。例えば身体活動レベルが低い女性の場合、1日のエネルギー消費は1,400～2,000kcal程度です。しかし運動により活動量を増やすと、これが1,800～2,400kcal程度までアップします。また有酸素運動には、血中脂質を分解したり、内臓の脂肪細胞を小さくしたりする効果もあります。そのため、食事のコントロールに運動をプラスすることで、より有効なダイエットが可能です。特に食べすぎてしまった次の日は、いつもより一駅分多めに歩く、意識的にストレッチをするなど、運動をしましょう。"),
        ("4. 早めに夕食を摂ってたっぷり寝る", "https://nosh.jp/magazine/wp-content/uploads/2022/10/th_%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB-8-740x493.jpg.webp", "睡眠とエネルギー代謝には深い関わりがあります。そのため、睡眠不足は肥満の発症と関連しているとされています。米国の研究では、睡眠時間の短縮が、腹部の脂肪の蓄積につながるという結果が示されました。よって、食べすぎをリセットするために、意識して早く眠りましょう。早く眠れば、睡眠時の代謝でエネルギーを消費でき、強制的に食べられない状況も作ることもできます。なお、就寝の直前に夕食を摂ると、消化活動が睡眠を妨げてしまいます。そのため、夕食はできるだけ早めに済ませるのがおすすめです。")
    ]
    for tip_title, image_url, tip_content in tips:
        with st.expander(tip_title):
            st.write(tip_content)
            try:
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                st.image(image, caption=tip_title, use_column_width=True)
            except Exception as e:
                st.write("画像の読み込みに失敗しました。")
                st.write(e)



def main():
    gender = st.selectbox("性別を選択してください", ["男性", "女性"])
    age = st.number_input("年齢を入力してください", min_value=0, max_value=150, value=30)
    weight = st.number_input("体重(kg)を入力してください", min_value=0.0, max_value=300.0, value=60.0)
    height = st.number_input("身長(cm)を入力してください", min_value=0.0, max_value=300.0, value=170.0)
    activity_level = st.selectbox("身体レベルを選んでください",["ほとんど運動しない", "軽い運動", "運動量が普通", "運動量が高い"])

    if st.button("計算"):
        if activity_level == "ほとんど運動しない":
            activity_level = 1
        elif activity_level == "軽い運動":
            activity_level = 2
        elif activity_level == "運動量が普通":
            activity_level = 3
        elif activity_level == "運動量が高い":
            activity_level = 4

        calorie = calculate_calorie(gender, age, weight, height / 100, activity_level)
        st.write(f"あなたの消費カロリーは {calorie:.2f} kcalです。")
        
        meal_recommendation, image_url = recommend_meal(calorie)
        st.write("おすすめの食事:")
        st.write(meal_recommendation)
        
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption='おすすめの食事', use_column_width=True)
        except Exception as e:
            st.write("画像の読み込みに失敗しました。")
            st.write(e)
        
        display_overeating_tips()

if __name__ == "__main__":
    main()
