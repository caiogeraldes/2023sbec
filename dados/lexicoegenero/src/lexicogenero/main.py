import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Any, Dict
from dotenv import load_dotenv
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    log_loss,
)
from cltk.alphabet.grc import normalize_grc
from lexicogenero.ferramentas.diorisis_reader import (
    carrega_textos,
    em_pandas,
    sent_pandas,
)
from lexicogenero.ferramentas.data import gera_hist_filo, gera_paragrafo, gera_sent
from lexicogenero.grc import STOPS_LIST

import logging

logging.basicConfig(
    filename="data/log.log",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)

# Carrega path para o Diorisis a depender do especificado em ../.env,
# rompe runtime caso não esteja especificada.
load_dotenv()
DIORISIS_PATH = os.getenv("DIORISIS_PATH")
assert DIORISIS_PATH is not None, "Path para DIORISIS não especificada"
FIGURAS_PATH = os.getenv("FIGURAS_PATH")
assert FIGURAS_PATH is not None, "Path para FIGURAS não especificada"

if __name__ == "__main__":
    plt.rcParams["figure.figsize"] = [20, 5]
    plt.style.use("ggplot")
    sns.set_palette("Dark2")

    print("Gerando banco de dados")
    logging.info("Gerando banco de dados")

    DATA = "./data/data_classico.csv"
    SENTS = "./data/sents_classico.csv"
    if os.path.exists(DATA) and os.path.exists(SENTS):
        print(f"Carregando arquivos:\n\t{DATA}\n\t{SENTS}")
        logging.info(f"Carregando arquivos:\n\t{DATA}\n\t{SENTS}")
        df_tokens = pd.read_csv(DATA)
        df_sents = pd.read_csv(SENTS)
    else:
        ignorados = [
            "Xenophon (0032) - On the Art of Horsemanship (013).json",
            "Xenophon (0032) - Economics (003).json",
            "Xenophon (0032) - Ways and Means (011).json",
            "Xenophon (0032) - Constitution of the Lacedaemonians (010).json",
            "Xenophon (0032) - On the Cavalry Commander (012).json",
            "Xenophon (0032) - On Hunting (014).json",
            "Xenophon (0032) - Apology (005).json",
            "Plato (0059) - Lovers (016).json",  # Espúrios
            "Plato (0059) - Epistles (036).json",
            "Plato (0059) - Alcibiades 1 (013).json",
            "Plato (0059) - Alcibiades 2 (014).json",  # Anotação problemática
            "Plato (0059) - Cleitophon (029).json",
            "Plato (0059) - Epinomis (035).json",
            "Plato (0059) - Hipparchus (015).json",
            "Plato (0059) - Menexenus (028).json",
            "Plato (0059) - Minos (033).json",
            "Plato (0059) - Theages (017).json",
        ]

        corpus = carrega_textos(
            autores=[
                "Herodotus",
                "Thucydides",
                "Plato",
                "Xenophon (0032)",  # Exclui Xenofonte de Éfeso
            ],
            diorisis_path=DIORISIS_PATH,
            ignore=ignorados,
            verbose=False,
        )
        df_tokens = em_pandas(corpus)
        df_sents = sent_pandas(corpus)
        del corpus

        print(f"Salvando dados em tokens em {DATA}")
        logging.info(f"Salvando dados em tokens em {DATA}")
        df_tokens.to_csv(DATA, index=False)
        print(f"Salvando dados em sentenças em {SENTS}")
        logging.info(f"Salvando dados em sentenças em {SENTS}")
        df_sents.to_csv(SENTS, index=False)

    df_tokens.dropna(inplace=True)
    df_sents.dropna(inplace=True)

    print("Normalizando dados")
    logging.info("Normalizando dados")
    df_sents["lemmata"] = df_sents["lemmata"].apply(normalize_grc)
    df_tokens["lemma"] = df_tokens["lemma"].apply(normalize_grc)

    print("Anotando gênero")
    logging.info("Anotando gênero")
    lst_hist = [
        "Herodotus (0016) - Histories (001).json",
        "Xenophon (0032) - Hellenica (001).json",
        "Xenophon (0032) - Cyropaedia (007).json",
        "Xenophon (0032) - Anabasis (006).json",
        "Thucydides (0003) - History (001).json",
    ]

    df_tokens = gera_hist_filo(df_tokens, lst_hist)
    df_sents = gera_hist_filo(df_sents, lst_hist)

    print("Separando subcorpora")
    logging.info("Separando subcorpora")
    df_verbos = df_tokens.loc[
        (df_tokens.POS == "verb") & (-df_tokens.lemma.isin(STOPS_LIST)),
    ]
    df_verbos_sent = gera_sent(df_verbos)
    df_verbos_par = gera_paragrafo(df_verbos)

    df_subst = df_tokens.loc[
        (df_tokens.POS == "noun") & (-df_tokens.lemma.isin(STOPS_LIST)),
    ]
    df_subst_sent = gera_sent(df_subst)
    df_subst_par = gera_paragrafo(df_subst)

    df_tokens_par = gera_paragrafo(df_tokens.loc[df_tokens.POS != "punct"])

    x_dpv, y_dpv = df_verbos_par.lemma, df_verbos_par.genero

    print("Treinando modelo de uso")
    logging.info("Treinando modelo de uso")
    verbos_dgci = set(
        [
            normalize_grc(x)
            for x in [
                "ἀνίημι",
                "δέομαι",
                "δοκέω",
                "ἐγχωρέω",
                "ἐκγίγνομαι",
                "ἔνειμι",
                "ἐντέλλω",
                "ἔοικα",
                "ἔξεστι",
                "ἐπαγγέλλω",
                "ἐπαινέω",
                "ἐπιβάλλω",
                "ἐπισκήπτω",
                "ἐπιτάσσω",
                "ἐπιτέλλω",
                "ἐπαινέω",
                "ἱκετεύω",
                "καταδικάζω",
                "κηρύσσω",
                "παραγγέλλω",
                "παραιτέω",
                "παραιτέομαι",
                "παραμυθέομαι",
                "παρίημι",
                "πιστεύω",
                "πόρω",
                "πρέπει",
                "πρέπω",
                "προβάλλω",
                "προξενέω",
                "προσδέομαι",
                "προσήκει",
                "προστάσσω",
                "προσχρῄζω",
                "προτίθημι",
                "σημαίνω",
                "συγγιγνώσκω",
                "συμβαίνω",
                "συμβουλεύω",
                "συμπίπτω",
                "ὑπάρχω",
                "ὐφίημι",
                "χρῄζω",
                "χρῄζω",
                "ὑπάρχω",
                "ἐπισκήπτω",
                "παραγγέλλω",
                "ἐγχωρέω",
                "προσήκω",
                "συμβουλεύω",
                "ἐξαρκέω",
                "ἔξεστι",
                "συμφέρω",
                "ἀφίημι",
                "δίδωμι",
                "δέομαι",
                "δοκέω",
                "ἐντέλλω",
            ]
        ]
    )

    pipe = Pipeline(
        steps=[
            (
                "vectorizer",
                TfidfVectorizer(ngram_range=(1, 1),
                                stop_words=STOPS_LIST, binary=True),
            ),
            ("bayes", MultinomialNB()),
        ]
    )

    x_treino, x_teste, y_treino, y_teste = train_test_split(
        x_dpv, y_dpv, test_size=0.2, shuffle=True, random_state=169
    )

    pipe.fit(x_treino, y_treino)

    vectorizer: Any = pipe["vectorizer"]
    bayes: Any = pipe["bayes"]

    y_pred = pipe.predict_proba(x_treino)

    print(classification_report(y_pred=pipe.predict(x_teste), y_true=y_teste))
    logging.info(classification_report(
        y_pred=pipe.predict(x_teste), y_true=y_teste))
    print(
        f"log loss: {log_loss(y_true=y_treino, y_pred=y_pred, labels=['filo', 'hist'])}"
    )
    logging.info(
        f"log loss: {log_loss(y_true=y_treino, y_pred=y_pred, labels=['filo', 'hist'])}"
    )

    plt.figure(figsize=(15, 10))
    sns.set(font_scale=1.5)

    cm = pd.DataFrame(confusion_matrix(y_pred=pipe.predict(x_teste), y_true=y_teste))
    cm.rename({0: "Filosofia", 1: "Historiografia"}, inplace=True)
    cm.rename({0: "Filosofia", 1: "Historiografia"}, axis=1, inplace=True)
    print(cm)
    sns.heatmap(
        cm,
        annot=True,
        fmt=""
    )
    plt.title("Matriz de confusão")
    plt.ylabel("Real")
    plt.xlabel("Previsão")
    plt.savefig(
        os.path.join(FIGURAS_PATH, "confusao.png"),
        bbox_inches="tight",
    )

    feature_log_prob_hist: Dict[str, float] = {}
    for ngram, index in vectorizer.vocabulary_.items():
        feature_log_prob_hist[ngram] = bayes.feature_log_prob_[1][index]

    flp_hist = [
        {"genero": "hist", "lemma": lemma,
            "logprob": feature_log_prob_hist[lemma]}
        for lemma in sorted(
            feature_log_prob_hist, key=feature_log_prob_hist.get, reverse=True  # type: ignore
        )
        if lemma in verbos_dgci
    ]

    df_flp_hist = pd.DataFrame(flp_hist)

    df_flp_hist["z"] = abs(
        (df_flp_hist.logprob - pd.Series(bayes.feature_log_prob_[1]).mean())
        / pd.Series(bayes.feature_log_prob_[1]).std()
    )

    feature_log_prob_filo = {}
    for ngram, index in vectorizer.vocabulary_.items():
        feature_log_prob_filo[ngram] = bayes.feature_log_prob_[0][index]

    flp_filo = [
        {"genero": "filo", "lemma": lemma,
            "logprob": feature_log_prob_filo[lemma]}
        for lemma in sorted(
            feature_log_prob_filo, key=feature_log_prob_filo.get, reverse=True  # type: ignore
        )
        if lemma in verbos_dgci
    ]

    df_flp_filo = pd.DataFrame(flp_filo)

    df_flp_filo["z"] = abs(
        (df_flp_filo.logprob - pd.Series(bayes.feature_log_prob_[0]).mean())
        / pd.Series(bayes.feature_log_prob_[0]).std()
    )

    df_flp = df_flp_filo._append(df_flp_hist).reset_index()
    print("Salvando resultados em ./data/data_flp.csv")
    logging.info(
        "Salvando resultados em ./data/data_flp.csv"
    )
    df_flp.to_csv(
        "./data/data_flp.csv", index=False)

    sns.set_palette("Dark2")
    plt.figure(figsize=(15, 25))
    bar = sns.barplot(
        data=df_flp.sort_values("lemma"),
        y="lemma",
        x="logprob",
        hue="genero",
        orient="horiz",
    )
    for i, (z, p) in enumerate(
        zip(
            df_flp.sort_values("lemma").z, df_flp.sort_values("lemma").logprob
        )  # type: ignore
    ):
        bar.text(0, (i / 2) - 0.1, str(round(z, 2)), fontdict={"fontsize": 15})
    plt.title("Probabilidade em log de cada lemma")
    plt.savefig(
        os.path.join(FIGURAS_PATH, "logprobs.png"),
        bbox_inches="tight",
    )

    df_flp_filo.set_index("lemma", inplace=True)
    df_flp_hist.set_index("lemma", inplace=True)
    diffs = (df_flp_filo.logprob - df_flp_hist.logprob).reset_index()
    diffs["z"] = (df_flp_filo.z - df_flp_hist.z).to_frame().reset_index().z
    diffs["modal"] = [
        bool(x)
        for x in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, ]
    ]
    print(
        "Salvando resultados em ./data/data_diff.csv"
    )
    logging.info(
        "Salvando resultados em ./data/data_diff.csv"
    )
    diffs.to_csv(
        "./data/data_diff.csv", index=False)

    plt.figure(figsize=(20, 7))
    sns.set(font_scale=1.2)

    chart = sns.barplot(
        data=diffs.sort_values("logprob"), x="lemma", y="logprob", palette="viridis"
    )
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.savefig(
        os.path.join(FIGURAS_PATH, "diff.png"), bbox_inches="tight"
    )

    plt.figure(figsize=(20, 7))
    sns.set(font_scale=1.2)

    chart2 = sns.barplot(
            data=diffs.sort_values("logprob"),
            x="lemma",
            y="logprob",
            hue="modal",
            dodge=False,
            palette="viridis")
    chart2.set_xticklabels(chart.get_xticklabels(), rotation=45, horizontalalignment='right')
    plt.savefig(
        os.path.join(FIGURAS_PATH, "diff2.png"), bbox_inches="tight"
    )

    print(
        df_flp[["genero", "lemma", "logprob", "z"]]
        .groupby(["lemma", "genero"])
        .agg(lambda x: x)
    )
    logging.info(
        df_flp[["genero", "lemma", "logprob", "z"]]
        .groupby(["lemma", "genero"])
        .agg(lambda x: x)
    )
    sns.displot(diffs.z.apply(abs), kde=True,
                aspect=1.5, palette="Dark2", bins=10)
    plt.yticks(ticks=[0, 2, 4, 6, 8, 10, 12, 14])
    plt.xlabel("Diferença absoluta de z")
    plt.ylabel("Conta")
    plt.axvline(diffs.z.apply(abs).quantile(0.95), color="black")
    plt.savefig(
        os.path.join(FIGURAS_PATH, "diffz.png"), bbox_inches="tight"
    )
