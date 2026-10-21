# REML fits, D-study and parametric bootstrap for run_analysis.py (lme4).
# Called as: Rscript gtheory_models.R <work_dir> <B> <B_persons>
# Reads  <dir>/scores.csv: one row per answer and method (response_id, person_id, question_id, activation, method,
#        score_z, quality_other, length_other)
# Writes <dir>/components.csv (model, component, variance, singular), <dir>/fixed.csv (model, term, estimate, se),
#        <dir>/stats.csv (model, stat, estimate, ci_lo, ci_hi; CIs when B > 0, percentile, B parametric draws;
#        share of person variance left by each covariate set, CI from B_persons person-cluster resamples)
suppressPackageStartupMessages(library(lme4))
args <- commandArgs(trailingOnly = TRUE)
dir <- args[1]
B <- if (length(args) > 1) as.integer(args[2]) else 0L
B_persons <- if (length(args) > 2) as.integer(args[3]) else 0L
set.seed(20261021)

d <- read.csv(file.path(dir, "scores.csv"))
d$method <- factor(d$method, levels = c("evidence_weighted", "zero_shot"))
d$activation <- factor(d$activation)
for (v in c("person_id", "question_id", "response_id")) d[[v]] <- factor(d[[v]])
d$pm <- interaction(d$person_id, d$method, drop = TRUE)
d$qm <- interaction(d$question_id, d$method, drop = TRUE)
d$pq <- interaction(d$person_id, d$question_id, drop = TRUE)
d$pa <- interaction(d$person_id, d$activation, drop = TRUE)
dc <- d[complete.cases(d[, c("quality_other", "length_other")]), ]   # persons with both covariates

ctrl <- lmerControl(calc.derivs = FALSE, check.conv.singular = "ignore")
names_map <- c(person_id = "person", pa = "person:activation", question_id = "question", pm = "person:method",
               qm = "question:method", pq = "person:question", response_id = "answer", Residual = "residual")
base <- " + (1 | person_id) + (1 | question_id) + (1 | pm) + (1 | qm) + (1 | pq)"
joint <- paste0(base, " + (1 | pa)")
lvl <- " + (1 | response_id) + (1 | question_id) + (1 | qm)"

fits <- list(base = list(paste0("score_z ~ method", base), d),
             joint = list(paste0("score_z ~ method * activation", joint), d))
for (a in levels(d$activation)) {
  fits[[paste0("level_", a)]] <- list(paste0("score_z ~ method", lvl), d[d$activation == a, ])
  fits[[paste0("level_", a, "_quality")]] <- list(paste0("score_z ~ method * quality_other", lvl),
                                                  dc[dc$activation == a, ])
}
covs <- list(none = character(0), length = "length_other", quality = "quality_other",
             quality_length = c("quality_other", "length_other"))
for (nm in names(covs)) {
  rhs <- if (length(covs[[nm]])) paste0(" + method * (", paste(covs[[nm]], collapse = " + "), ")") else ""
  fits[[paste0("cov_", nm)]] <- list(paste0("score_z ~ method * activation", rhs, joint), dc)
}

comp <- list(); fx <- list(); models <- list()
for (nm in names(fits)) {
  f <- lmer(as.formula(fits[[nm]][[1]]), data = fits[[nm]][[2]], REML = TRUE, control = ctrl)
  models[[nm]] <- f
  v <- as.data.frame(VarCorr(f))
  comp[[nm]] <- data.frame(model = nm, component = names_map[v$grp], variance = v$vcov, singular = isSingular(f))
  cf <- summary(f)$coefficients
  fx[[nm]] <- data.frame(model = nm, term = rownames(cf), estimate = cf[, 1], se = cf[, 2])
}
write.csv(do.call(rbind, comp), file.path(dir, "components.csv"), row.names = FALSE)
write.csv(do.call(rbind, fx), file.path(dir, "fixed.csv"), row.names = FALSE)

# Statistics per model. D-study (methods random): relative error s2_pm/n_m + s2_pq/n_q + s2_res/(n_q n_m);
# absolute error adds s2_q/n_q + s2_qm/(n_q n_m). Joint model, activation fixed, n_q questions spread evenly over the
# n_a levels: universe score s2_p + s2_pa/n_a. Level models: agreement = s2_answer / (s2_answer + s2_res).
n_a <- nlevels(d$activation)
vc <- function(f) { v <- as.data.frame(VarCorr(f)); setNames(v$vcov, names_map[v$grp]) }
sig <- function(x) setNames(x, paste0("sigma2_", names(x)))
stat_base <- function(f) {
  x <- vc(f); out <- sig(x)
  for (nm in 1:2) for (nq in c(1, 2, 3, 4, 6, 8, 10, 12)) {
    rel <- x[["person:method"]] / nm + x[["person:question"]] / nq + x[["residual"]] / (nq * nm)
    abs <- rel + x[["question"]] / nq + x[["question:method"]] / (nq * nm)
    out[paste0("erho2_m", nm, "_q", nq)] <- x[["person"]] / (x[["person"]] + rel)
    out[paste0("phi_m", nm, "_q", nq)] <- x[["person"]] / (x[["person"]] + abs)
  }
  out
}
stat_joint <- function(f) {
  x <- vc(f); out <- sig(x)
  un <- x[["person"]] + x[["person:activation"]] / n_a
  for (nm in 1:2) for (nq in c(3, 6, 9, 12)) {
    rel <- x[["person:method"]] / nm + x[["person:question"]] / nq + x[["residual"]] / (nq * nm)
    out[paste0("erho2_m", nm, "_q", nq)] <- un / (un + rel)
  }
  out
}
stat_level <- function(f) {
  x <- vc(f)
  c(sig(x), agreement = x[["answer"]] / (x[["answer"]] + x[["residual"]]))
}
stat_cov <- function(f) c(sigma2_person = vc(f)[["person"]])
stat_fun <- function(nm) {
  if (nm == "base") stat_base else if (nm == "joint") stat_joint
  else if (grepl("^level_[0-9]+$", nm)) stat_level else stat_cov
}
targets <- c("base", "joint", paste0("level_", levels(d$activation)), paste0("cov_", names(covs)))
st <- list()
for (nm in targets) {
  FUN <- stat_fun(nm)
  est <- FUN(models[[nm]])
  lo <- hi <- rep(NA_real_, length(est))
  if (B > 0) {
    b <- bootMer(models[[nm]], FUN, nsim = B, type = "parametric", use.u = FALSE)
    lo <- apply(b$t, 2, quantile, 0.025, na.rm = TRUE)
    hi <- apply(b$t, 2, quantile, 0.975, na.rm = TRUE)
  }
  st[[nm]] <- data.frame(model = nm, stat = names(est), estimate = unname(est), ci_lo = unname(lo), ci_hi = unname(hi))
}

# Share of person variance left = person variance with a covariate set / without; persons resampled with replacement
person_var <- function(nm, data) vc(lmer(as.formula(fits[[paste0("cov_", nm)]][[1]]), data = data, REML = TRUE,
                                         control = ctrl))[["person"]]
sets <- names(covs)[-1]
share_est <- sapply(sets, function(nm) vc(models[[paste0("cov_", nm)]])[["person"]] / vc(models[["cov_none"]])[["person"]])
share_lo <- share_hi <- rep(NA_real_, length(sets))
if (B_persons > 0) {
  persons <- levels(droplevels(dc$person_id))
  resample <- function() {
    pick <- sample(persons, length(persons), replace = TRUE)
    s <- do.call(rbind, lapply(seq_along(pick), function(i) {
      x <- dc[dc$person_id == pick[i], ]
      x$person_id <- paste0(pick[i], "_", i)
      x
    }))
    s$person_id <- factor(s$person_id)
    s$pm <- interaction(s$person_id, s$method, drop = TRUE)
    s$pq <- interaction(s$person_id, s$question_id, drop = TRUE)
    s$pa <- interaction(s$person_id, s$activation, drop = TRUE)
    pv <- sapply(names(covs), person_var, data = s)
    pv[sets] / pv[["none"]]
  }
  draws <- t(replicate(B_persons, resample()))
  share_lo <- apply(draws, 2, quantile, 0.025, na.rm = TRUE)
  share_hi <- apply(draws, 2, quantile, 0.975, na.rm = TRUE)
}
st[["share"]] <- data.frame(model = paste0("cov_", sets), stat = "share_left", estimate = unname(share_est),
                            ci_lo = unname(share_lo), ci_hi = unname(share_hi))
write.csv(do.call(rbind, st), file.path(dir, "stats.csv"), row.names = FALSE)
