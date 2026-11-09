# SourceTrace

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | **Italiano** | [العربية](README.ar.md)

> Questo testo è una traduzione di [README.md](README.md) fatta con l'IA. In caso di differenze, vale la versione inglese.

Un Agent Skill che verifica un albero della conoscenza generato dall'IA confrontandolo con le slide da cui è stato ricavato.

Gli strumenti di IA trasformano le slide di una lezione in un albero della conoscenza in pochi secondi, ma una definizione può essere sbagliata, una relazione può essere inventata e qualcosa di importante può mancare. SourceTrace controlla ogni nodo e ogni arco rispetto alle immagini originali e motiva ogni verdetto con prove: **perché** è un problema, **dove** si trova nelle slide (pagina e citazione) e **su cosa** si basa (ID delle prove).

Funziona con gli strumenti che supportano gli Agent Skills, come Claude Code o Codex, e gestisce slide o screenshot di pagine web in cinese o in inglese.

## Cosa si ottiene

Gli si danno le immagini delle slide (PNG/JPG) e l'albero della conoscenza (JSON). Scrive tre file in `sourcetrace-output/`, accanto all'albero:

| File | Contenuto |
|------|---------|
| `report.md` | Il rapporto di verifica: riepilogo, problemi, note sulla fonte (compresse), omissioni, problemi di struttura, elementi confermati |
| `audit.json` | Lo stesso risultato in forma leggibile da una macchina: un verdetto per ogni nodo e ogni arco |
| `evidence-index.json` | Tutto ciò che è stato estratto dalle slide, ogni elemento con ID, pagina e citazione testuale |

Due problemi trovati in un'esecuzione su 8 slide in cinese (il rapporto è in cinese), con il testo accorciato e senza la colonna dei suggerimenti ([rapporto completo](tests/smoke/model-eval-e2e/report.md)):

| 编号 | 对象 | 类别 | 风险 | 问题 | 证据 |
|---|---|---|---|---|---|
| F-002 | N005 数据集划分比例 | 概念错误 | 高 | 比例数字错误：树中写"8 : 1 : 1"，课件写"7 : 2 : 1"。 | EV-013 第 2 页 "本课程推荐的划分比例：训练集 : 验证集 : 测试集 = 7 : 2 : 1。" |
| F-004 | E010 过拟合 —related-to→ 高偏差 | 关系错误 | 高 | 关系对调：第 4 页图示为"过拟合 → 高方差"，树中却把过拟合连到高偏差。 | EV-020 第 4 页 "Diagram: 过拟合 → 高方差（对训练数据过于敏感）" |

Ogni problema riceve una di sei categorie (errore concettuale, relazione errata, estensione non supportata, generalizzazione eccessiva, non verificabile, omissione) e un livello di rischio, e ogni problema include una correzione suggerita. Una definizione che la fonte supporta, tranne un dettaglio aggiunto, non viene considerata un errore: compare come *nota sulla fonte* a basso rischio, in una sezione compressa a parte.

## Per iniziare

1. Installare l'unica dipendenza:

   ```bash
   pip install jsonschema
   ```

2. Copiare la cartella `source-trace/` nella cartella degli skill del proprio strumento:

   | Strumento | Cartella degli skill |
   |------|---------------|
   | Claude Code (personale) | `~/.claude/skills/source-trace/` |
   | Claude Code (un progetto) | `<project>/.claude/skills/source-trace/` |
   | Codex | `~/.codex/skills/source-trace/` (controllare la documentazione della propria versione di Codex) |

3. Chiedere con parole proprie, indicando le immagini delle slide e l'albero:

   > 这是我的课件截图（slides/ 文件夹）和 AI 生成的知识树 tree.json，帮我对照课件检查一下。

   > Check knowledge-tree.json against my lecture slides in images/.

L'albero deve seguire [`knowledge-tree.schema.json`](source-trace/schemas/knowledge-tree.schema.json) (nodi con `id`, `label`, `definition`, `kind`; archi con `id`, `source`, `target`, `relation`). Se il vostro usa un altro formato, lo skill lo converte prima e dice come ha fatto la corrispondenza. Le slide in PPT o PDF vanno prima esportate come immagini.

## Privacy

SourceTrace funziona dentro l'agente di IA, quindi l'agente legge le immagini delle slide e l'albero della conoscenza. Questi vengono inviati al modello di IA usato dall'agente, alle condizioni di quel fornitore. Gli script dello skill funzionano in locale e non inviano nulla.

- **Verificare solo slide che si è autorizzati a condividere** con il proprio fornitore di IA. Le slide di un corso di solito appartengono al docente, quindi può servire il suo permesso.
- **Trattare i risultati come le slide stesse.** `evidence-index.json` e `report.md` contengono citazioni testuali delle slide.
- **Non pubblicare né inserire in un repository le slide o i risultati di verifica di altri** senza permesso.

## Quanto funziona

**Slide sintetiche.** Su due insiemi di test con errori inseriti apposta (4 slide in inglese, 8 slide in cinese), sia un normale assistente di IA sia SourceTrace hanno trovato tutti gli errori inseriti. SourceTrace aggiunge ciò che al modello normale manca:

- ID delle prove, pagine e citazioni dietro ogni verdetto,
- un verdetto per ogni nodo e ogni arco,
- categorie e livelli di rischio fissi,
- un `audit.json` leggibile da una macchina,
- nessuna voce "mancante" fuori tema,
- lo stesso risultato in tutte e quattro le esecuzioni sull'insieme in cinese.

Costa circa il 30% di token in più e richiede circa il triplo del tempo.

**Contenuti reali.** Voci di Wikipedia in cinese (CC BY-SA 4.0), con alberi della conoscenza generati da altri strumenti di IA, quindi gli errori sono reali. Per le prime due voci, con alberi di OpenAI Codex, il responsabile del progetto ha esaminato ogni rapporto, e le regole sono state riviste dopo ogni esame:

| Esecuzione | Elementi giudicati | Corretti | In parte corretti | Sbagliati |
|-----|--------------|---------|----------------|-------|
| 机器学习 (apprendimento automatico), esecuzione 1 (regole v0.1.0) | 13 | 6 | 4 | 3 |
| 机器学习 (apprendimento automatico), esecuzione 2 (prima revisione) | 18 | 14 | 1 | 3 |
| 决策树学习 (apprendimento con alberi di decisione), esecuzione 1 (seconda revisione) | 11 problemi + 77 elementi confermati | 85 | 1 | 2 |

Dopo la v0.2.0 (dettagli in [CHANGELOG.md](CHANGELOG.md)):

- **Altre due voci** con la quinta revisione delle regole. 朴素贝叶斯分类器 (classificatore bayesiano ingenuo, albero di ChatGPT): due nuove esecuzioni hanno concordato con la soluzione su tutti gli 87 elementi. 感知器 (percettrone, albero di Codex): entrambe le esecuzioni hanno trovato i due errori reali dell'albero e non hanno segnalato nessun elemento corretto, ma non hanno visto quattro problemi della fonte stessa che richiedono una breve derivazione. Le soluzioni di queste due voci sono revisioni fatte dall'IA e accettate dal responsabile; quella di 朴素贝叶斯分类器 viene dalla stessa conversazione che ha generato l'albero.
- **Un test di scala** (32 slide sintetiche, un albero di 169 elementi), **immagini degradate** (versioni simili a scansioni, a foto e parzialmente coperte) e **una prima esecuzione con Codex**.

La sesta revisione delle regole non è ancora stata eseguita, e tutte le revisioni sono state fatte o accettate da una sola persona. Dettagli e limiti: [docs/evaluation.md](docs/evaluation.md) (fino alla v0.2.0) e il file `RESULTS.md` di ogni insieme di test.

## Come funziona

SourceTrace procede in sei fasi: acquisizione della fonte → estrazione delle prove → mappatura della conoscenza → verifica nei due sensi → rilevamento dei conflitti → rapporto di verifica. L'agente svolge le parti che richiedono giudizio: leggere le slide, abbinare le affermazioni alle prove e scegliere i verdetti. Tre script fanno tutto ciò che si può controllare o calcolare:

| Script | Fase | Cosa fa |
|--------|-------|------|
| `validate_input.py` | 1 | Controlla l'albero e le immagini, numera le pagine e avvisa dei problemi di struttura, per esempio un albero non connesso |
| `validate_evidence.py` | 2 | Controlla l'indice delle prove: ID univoci, pagine e fonti coerenti |
| `build_report.py` | 6 | Controlla l'`audit.json` dell'agente rispetto all'albero e alle prove, aggiunge il riepilogo e gli ID dei problemi e genera `report.md` |

Le regole per verdetti, categorie, rischio e omissioni sono in [`references/audit-rules.md`](source-trace/references/audit-rules.md). Le scelte di progetto alla loro base sono in [docs/requirements.md](docs/requirements.md).

Gli script si possono anche eseguire da soli:

```bash
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
python source-trace/scripts/validate_evidence.py --index tests/fixtures/ml-basics/evidence-index.example.json
python source-trace/scripts/build_report.py --tree <tree.json> --index <output>/evidence-index.json --audit <output>/audit.json
```

I due validatori accettano `--json` per un output leggibile da una macchina. `validate_input.py` scrive i percorsi delle immagini relativi alla cartella di output (`sourcetrace-output/` accanto all'albero, o la cartella indicata con `--out`). Tutti e tre gli script terminano con 0 in caso di successo, 1 con un input non valido e 2 con un errore d'uso.

## Sviluppo

```bash
pip install -r requirements.txt
python -m pytest
```

119 test, circa 2 secondi. Coprono i tre script (input valido, ogni codice di errore e di avviso, output ripetibile, rapporti in cinese e in inglese) e controllano che le esecuzioni dello skill salvate rispettino ancora le soluzioni. Non eseguono lo skill stesso, che richiede un agente; per valutare nuove esecuzioni si usa `tools/compare_runs.py`.

```
source-trace/          lo skill (è questa la cartella da installare)
├── SKILL.md           istruzioni e descrizione di attivazione
├── schemas/           JSON Schema: albero della conoscenza, elemento di prova, indice delle prove, verifica
├── references/        regole di estrazione e di verifica, caricate quando servono
└── scripts/           i tre script descritti sopra
docs/                  requisiti e valutazione
tests/fixtures/        insiemi di test: slide sintetiche con soluzioni; screenshot di Wikipedia (CC BY-SA) con esecuzioni e revisioni
tests/baseline/        esecuzioni con un'IA normale, per confronto
tests/smoke/           esecuzioni complete dello skill
tests/consistency/     esecuzioni ripetute dello skill
tests/test_*.py        la suite pytest
tools/                 make_fixture_slides.py, compare_runs.py, degrade_images.py
```

## Stato e prossimi passi

v0.2.0, con modifiche successive non ancora rilasciate. Vedere [CHANGELOG.md](CHANGELOG.md).

Politica sui dati di test: SourceTrace viene testato solo su materiale con licenza aperta, scritto dal responsabile del progetto o sintetico. Non si usano materiali di corsi di terzi né dati privati.

Prossimi passi:

1. **Di nuovo Codex:** eseguire la sesta revisione delle regole in Codex.
2. **Valutazione:** aggiornare [docs/evaluation.md](docs/evaluation.md) con i test successivi alla v0.2.0.
3. **Rilasciare la v0.3.0.**
4. **Modalità di lavoro** (più avanti): una modalità rigorosa di tracciamento delle fonti e una modalità di revisione che ammette brevi spiegazioni esterne alla fonte, segnalate come tali.

## Licenza

[MIT](LICENSE)
