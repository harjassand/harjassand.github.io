# Original AI-generated catalytic tensor proof narrative (11 October 2026)

> Exact source transcription from Astra's N680 proof candidate. The source's correctness, completeness of cited finite tests, historical originality and priority are not independently certified. This appendix is included as source evidence, not a second externally vetted manuscript.

Original source: https://github.com/harjassand/astra-research-knowledge/blob/main/updates/DK/package/catalytic_pivot_2026-10-11/source_packet/sources/Pasted%20markdown(20261011-042249).md

---

## Result: exact catalytic tensor conversion can encode arbitrary matrix algebra

I obtained a different kind of result: **a dimension-preserving construction that makes ordinary three-party tensor restriction simulate arbitrary finite-dimensional representations of finitely presented algebras.**

The resulting proposed theorem is substantially stronger than an obstruction to coefficient growth:

> **Exact conversion assisted by a returned bipartite catalyst is recursively enumerable–complete—even with fixed tensor formats, a fixed target, and a source varying along one fixed rank-one affine line. The input tensors can all have strictly positive integer coefficients.**

The proof is below. **Historical originality and independent mathematical verification remain unresolved.** I am not treating this as an independently validated historic breakthrough.

The mechanism does not suppress cancellation. It permits arbitrary complex local maps and uses **the locations and sizes of matrix-rank drops to force those maps to respect an encoded algebraic system**.

---

## 1. Precise statement

Work over \\(\mathbb C\\). Write a three-tensor in matrix slices:

\\[ T=\sum\_{i=0}^{q-1}e_i\otimes A_i. \\]

Define its amplification by a bipartite auxiliary state:

\\[ T[d]=\sum\_{i=0}^{q-1}e_i\otimes(A_i\otimes I_d). \\]

This places

\\[ \Phi_d=\sum\_{a=1}^{d}f_a\otimes f_a \\]

between the second and third parties, leaving the first party unassisted.

Write \\(T\succeq S\\) when three independent local linear maps convert \\(T\\) exactly into \\(S\\). Define

\\[ T\succeq\_{\mathrm{cat}}S \quad\Longleftrightarrow\quad \exists d\ge1:\ T[d]\succeq S[d]. \\]

The auxiliary state is returned exactly and uncorrelated with the target.

Operationally, this is **stochastic exact conversion**: the conversion succeeds with some nonzero probability, with no lower bound on that probability. It is not deterministic conversion or a requirement that the catalyst survive failed branches. Tensor restriction and stochastic multipartite entanglement conversion have an established connection; stochastic entanglement catalysis itself is not a new notion. [arXiv](https://arxiv.org/abs/1003.3059)

### Theorem A — Representation universality

There is an effective construction taking a finite presentation

\\[ \mathcal A= \mathbb Q\langle X_1,\ldots,X_t\rangle/ (p_1,\ldots,p_m) \\]

to integer three-tensors \\(T\_{\mathcal A},S\_{\mathcal A}\\), such that **for every positive integer \\(d\\)**,

\\[ \boxed{ \mathcal A\text{ has a unital representation in }M_d(\mathbb C) \iff T\_{\mathcal A}[d]\succeq S\_{\mathcal A}[d]. } \tag{1} \\]

The construction has polynomial encoding size when the relations are supplied as arithmetic circuits.

The representations need not be faithful.

### Theorem B — Fixed-format undecidability

There exist fixed integer three-tensors \\(U,V,S\\), with \\(U,V\\) of the same format and

\\[ \operatorname{rank}\_{\mathrm{tensor}}V=1, \\]

such that

\\[ \boxed{ \\{n\in\mathbb Z\_{\ge0}:U+nV\succeq\_{\mathrm{cat}}S\\} \text{ is recursively enumerable–complete.} } \tag{2} \\]

Moreover, \\(U,V,S\\) can all be chosen to have **strictly positive integer entries**.

“Recursively enumerable–complete” means that positive instances can eventually be recognized by a search, but deciding all instances is at least as hard as the halting problem.

The distinction from the previous matrix-multiplication result is fundamental: **the obstruction is now to decidability itself, not to stability or to a particular noise model.**

---

## 2. Proof of representation universality

### 2.1 Encode algebra relations as two-sided matrix equations

First replace higher-degree relations by quadratic relations, introducing a variable for each arithmetic-circuit gate. For example,

\\[ Z=XY,\qquad W=Z+Q \\]

become quadratic and linear relations. This preserves representations in every dimension: the auxiliary variables are determined by the original ones.

Clear rational denominators. Put

\\[ X_0=I,\qquad s=t+1. \\]

Every resulting relation can be written

\\[ p\_\nu(X)= \sum\_{a,b=0}^{t}c^{(\nu)}\_{ab}X_aX_b=0. \\]

Construct \\(s\times s\\) integer matrices \\(M_i\\), with corresponding scalars \\(b_i\\), as follows:

\\[ M_0=E\_{00},\qquad b_0=1; \\]

for every variable, include

\\[ E\_{a0}-E\_{0a},\qquad b=0; \\]

for every relation, include

\\[ M\_{p\_\nu}=\sum\_{a,b}c^{(\nu)}\_{ab}E\_{ab}, \qquad b=0. \\]

Finally include a distinguished index \\(\*\\) with

\\[ M\_\*=0,\qquad b\_\*=0. \\]

Consider rectangular unknowns

\\[ P=[P_0\ P_1\ \cdots\ P_t], \qquad Q= \begin{bmatrix} Q_0\\\Q_1\\\\\vdots\\\Q_t \end{bmatrix}, \\]

whose blocks are \\(d\times d\\), satisfying

\\[ P(M_i\otimes I_d)Q=b_iI_d \quad\text{for every }i. \tag{3} \\]

The normalization equation gives

\\[ P_0Q_0=I_d. \\]

Thus \\(P_0\\) is invertible and \\(Q_0=P_0^{-1}\\).

Set

\\[ X_a=P_0^{-1}P_a,\qquad Y_a=Q_aP_0. \\]

The equations corresponding to \\(E\_{a0}-E\_{0a}\\) force

\\[ X_a=Y_a. \\]

Consequently,

\\[ P(M\_{p\_\nu}\otimes I_d)Q = P_0p\_\nu(X)P_0^{-1}. \\]

Therefore (3) is equivalent to a \\(d\\)-dimensional unital representation of \\(\mathcal A\\).

Conversely, any representation gives a solution by taking

\\[ P=[I_d\ X_1\ \cdots\ X_t], \qquad Q= \begin{bmatrix} I_d\\\X_1\\\\\vdots\\\X_t \end{bmatrix}. \\]

The remaining problem is significant: **ordinary tensor restriction does not preserve slice labels or the rectangular blocks used in (3).** The next construction forces that preservation without restricting the allowed local maps.

### 2.2 Force slice labels using rank drops

Let \\(q\\) be the number of matrices \\(M_i\\), including the distinguished zero slice. For a coordinate vector \\(x=(x_i)\\), introduce the \\(2q-1\\) linear forms

\\[ x\_\*, \qquad x\_\*+x_i\quad(i\ne \*), \qquad 2x\_\*+x_i\quad(i\ne \*). \\]

Enumerate them as \\(\ell_1,\ldots,\ell\_{2q-1}\\). Define

\\[ h_j=(s+1)j, \qquad K=\sum_jh_j=(s+1)(2q-1)q, \\]

and

\\[ D(x)=\bigoplus\_{j=1}^{2q-1}\ell_j(x)I\_{h_j}. \tag{4} \\]

Now form the matrix pencils

\\[ A(x)=\left(\sum_i x_iM_i\right)\oplus D(x), \\]\\[ B(x)=\left(\sum_i x_ib_i\right)\oplus D(x). \tag{5} \\]

Their coefficient matrices define the source and target tensors. Their formats are

\\[ q\times(s+K)\times(s+K), \qquad q\times(1+K)\times(1+K). \\]

Suppose an arbitrary restriction

\\[ T\_{\mathcal A}[d]\succeq S\_{\mathcal A}[d] \\]

exists.

The target is concise in its first factor: if \\(B(x)=0\\), then every \\(\ell_j(x)=0\\), hence \\(x=0\\). Its first local map must therefore be invertible.

After changing the slice covector by an invertible matrix \\(G\\), the restriction implies

\\[ B(Gx)\otimes I_d = L\bigl(A(x)\otimes I_d\bigr)R. \tag{6} \\]

Here \\(R\\) incorporates the transpose of the third local map. Taking ranks and cancelling the factor \\(d\\),

\\[ \operatorname{rank}B(Gx) \le \operatorname{rank}A(x). \tag{7} \\]

Let

\\[ H_j=\ker\ell_j. \\]

For \\(x\in H_j\\),

\\[ \operatorname{rank}A(x) \le K-h_j+s\<K. \\]

But if \\(Gx\\) avoided every \\(H_k\\), its target marker block would have rank \\(K\\), contradicting (7).

Thus

\\[ G(H_j)\subseteq\bigcup_kH_k. \\]

Over \\(\mathbb C\\), a vector space cannot be covered by finitely many proper linear subspaces. Consequently,

\\[ G(H_j)=H\_{\pi(j)} \\]

for a permutation \\(\pi\\).

Choose a generic \\(x\in H_j\\), avoiding all other marker hyperplanes. Its image belongs to exactly \\(H\_{\pi(j)}\\). Equation (7) then gives

\\[ K-h\_{\pi(j)} \le K-h_j+s, \\]

or

\\[ h\_{\pi(j)}\ge h_j-s. \\]

Because consecutive \\(h_j\\)'s differ by \\(s+1\\),

\\[ \pi(j)\ge j. \\]

A permutation with this property is the identity.

Hence \\(G\\) preserves every labelled hyperplane. The forms

\\[ x\_\*,\quad x\_\*+x_i \\]

constitute a basis of the dual space. Preservation also of their sums

\\[ 2x\_\*+x_i=x\_\*+(x\_\*+x_i) \\]

forces their eigenvalues under the pullback by \\(G\\) to agree. Therefore

\\[ \boxed{G=\gamma I_q,\qquad \gamma\ne0.} \tag{8} \\]

Absorb this scalar into \\(L\\). Every individual slice equation is now fixed:

\\[ L(A_i\otimes I_d)R=B_i\otimes I_d. \tag{9} \\]

**This is the cancellation-resistant step.** It uses rank monotonicity and labelled rank drops, not positivity, coefficient bounds or restricted signs.

### 2.3 Prevent the marker blocks from simulating the algebra

There is still a possible loophole: the second and third local maps could mix the marker coordinates into the algebra coordinates.

The distinguished slice closes it.

At \\(x=e\_\*\\),

\\[ A\_\*=0_s\oplus D\_\*, \qquad B\_\*=0_1\oplus D\_\*, \\]

where \\(D\_\*=D(e\_\*)\\) is invertible: its diagonal blocks are \\(I\_{h_j}\\) or \\(2I\_{h_j}\\).

Partition the local maps according to source core and marker coordinates:

\\[ L=[L\_{\mathrm c}\ L\_{\mathrm m}], \qquad R= \begin{bmatrix} R\_{\mathrm c}\\\R\_{\mathrm m} \end{bmatrix}. \\]

The distinguished equation becomes

\\[ L\_{\mathrm m}(D\_\*\otimes I_d)R\_{\mathrm m} = \begin{pmatrix} 0&0\\\ 0&D\_\*\otimes I_d \end{pmatrix}. \tag{10} \\]

The right side has rank \\(Kd\\), exactly the maximum possible rank through the marker coordinates.

Therefore the column space of \\(L\_{\mathrm m}\\) is precisely the output marker space, and the row space of \\(R\_{\mathrm m}\\) is precisely the corresponding marker row space. In particular, their output-core components vanish.

Compressing every equation (9) to its first \\(d\\) output rows and columns now gives

\\[ P(M_i\otimes I_d)Q=b_iI_d. \\]

Section 2.1 extracts the required representation.

Conversely, any solution of these equations extends to the tensor restriction using

\\[ L=P\oplus I\_{Kd}, \qquad R=Q\oplus I\_{Kd}, \\]

and the identity on the first factor.

This proves (1), in both directions and for each \\(d\\).

The dimensions are polynomial in \\(s,q\\), and the construction consists of copying coefficients, matrix units and diagonal marker blocks. No unknown representation is used to construct the input tensors. ∎

---

## 3. From representation universality to the halting problem

Undecidability of unbounded finite-dimensional representation existence is already known; Letzter explicitly records this distinction between unrestricted dimension and fixed-dimensional algebraic decision problems. That source problem is **not** the proposed new contribution. [arXiv](https://arxiv.org/pdf/0708.3190)

For the stronger fixed-format, single-parameter conclusion, an explicit arithmetic encoding is useful.

### An integer-enforcing matrix system

Take generators \\(e,f,h,z\\) with

\\[ [h,e]=2e,\qquad [h,f]=-2f,\qquad [e,f]=h, \tag{11} \\]

require \\(z\\) to commute with every generator, and impose

\\[ z^2=(h+1)^2+4fe. \tag{12} \\]

The underlying \\(\mathfrak{sl}\_2\\) highest-weight construction is standard. [Webusers](https://webusers.imj-prg.fr/~michael.harris/Day3.pdf)

Consider a nonzero finite-dimensional simple complex module for an algebra containing these relations. Centrality makes \\(z=uI\\): an eigenspace of \\(z\\) is nonzero and invariant, so simplicity makes it the whole module.

Choose an \\(h\\)-eigenvector and repeatedly apply \\(e\\) until obtaining a nonzero vector \\(v\\) with

\\[ ev=0,\qquad hv=\lambda v. \\]

This terminates because nonzero successive vectors have distinct eigenvalues.

Let \\(m\\) be maximal with \\(f^mv\ne0\\). The commutator identity

\\[ ef^kv=k(\lambda-k+1)f^{k-1}v \\]

at \\(k=m+1\\) forces \\(\lambda=m\\). Applying (12) to \\(v\\),

\\[ u^2=(m+1)^2. \\]

Thus

\\[ \boxed{u\in\mathbb Z\setminus\\{0\\}.} \tag{13} \\]

Conversely, every nonzero integer \\(u\\) occurs. Put \\(m=|u|-1\\) and use a basis \\(v_0,\ldots,v_m\\) with

\\[ hv_j=(m-2j)v_j,\qquad fv_j=v\_{j+1}, \\]\\[ ev_j=j(m-j+1)v\_{j-1}, \qquad z=uI, \\]

with boundary vectors zero. Direct substitution verifies (11)–(12).

### Encode arbitrary integer polynomial equations

For every integer variable \\(x_i\\), introduce two commuting copies of this system, with central elements \\(u_i,v_i\\), and substitute

\\[ x_i=u_i-v_i. \\]

Every integer is a difference of two nonzero integers. Thus, for any integer polynomial \\(P\\), adjoining

\\[ P(u_1-v_1,\ldots,u_k-v_k)=0 \tag{14} \\]

gives an algebra having a nonzero finite-dimensional representation exactly when \\(P\\) has an integer root.

For the reverse direction, take a simple quotient of any finite-dimensional representation. All central elements become scalar nonzero integers, yielding the root. For the forward direction, tensor together the explicit representations above.

The passage to a simple quotient is important: it prevents non-scalar central matrices or nilpotent parts from creating false positive instances.

The Matiyasevich–Robinson–Davis–Putnam theorem supplies a **fixed** polynomial

\\[ P(n,x_1,\ldots,x_k) \\]

whose integer-root existence, as \\(n\ge0\\) varies, represents a recursively enumerable–complete set. Nonnegative-variable requirements can be eliminated using sums of four squares. Universal Diophantine equations are established prior art. [Cambridge University Press](https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/universal-diophantine-equation/113EBF3D928DFC6011C52BECAE81A087)

Introduce a generator \\(t\\) and impose

\\[ t-n1=0. \tag{15} \\]

All other relations use \\(t\\) symbolically, including

\\[ P(t,u_1-v_1,\ldots,u_k-v_k)=0. \\]

After quadraticization, **the number of generators and relations is fixed**, independently of \\(n\\). The only varying coefficient occurs in (15).

Applying Theorem A therefore yields fixed tensor formats and a fixed target \\(S\\). In the source, the varying contribution is

\\[ -n\\,e_r\otimes e_0\otimes e_0, \\]

where \\(r\\) labels relation (15). Hence the source is

\\[ U+nV \\]

with \\(V\\) rank one.

This proves recursively enumerable hardness.

For membership in the recursively enumerable class, fix \\(d\\). The local-map equations are a finite polynomial system over \\(\mathbb Q\\), with complex unknowns. Its solvability is decidable by algebraic elimination. Enumerating \\(d=1,2,\ldots\\) therefore recognizes every positive instance.

Thus (2) is recursively enumerable–complete. ∎

### Resource accounting

The input does not contain an infinite object or an oracle. In the fixed family, \\(n\\) has a binary encoding, and all source coefficients have bit length \\(O(\log(n+1))\\).

The unrestricted resources are the catalyst dimension and the entries of the local maps. For any specified \\(d\\), their existence is a finite algebraic decision problem.

**There is no efficiency claim for finding the catalyst or executing the conversion.**

---

## 4. Positive coefficients do not remove the obstruction

The rank-one affine family can be made strictly positive by fixed local changes of basis.

This matters because it shows that the undecidability cannot be attributed simply to negative coefficients in the input tensors.

In the construction above, relation \\(r\\) is \\(t-n1=0\\). Choose one coordinate \\(g\\) in the marker block associated with

\\[ x\_\*+x_r. \\]

Consider the three covectors

\\[ \alpha=2e\_\*^{\mathsf T}-e_r^{\mathsf T}, \qquad \beta=\gamma=e_0^{\mathsf T}+e_g^{\mathsf T}. \\]

For the fixed source tensors,

\\[ U(\alpha,\beta,\gamma)=1, \qquad V(\alpha,\beta,\gamma)=1. \tag{16} \\]

Indeed, the marker contribution to the first evaluation is \\(2-1\\), while the core term \\(E\_{t0}\\) contributes zero. The second evaluation follows from \\(V=-e_r\otimes e_0\otimes e_0\\).

Extend these covectors to invertible integer changes of basis. Now both tensors have corner coefficient \\(1\\).

Here is the remaining elementary construction. For an integer three-tensor \\(W\\) with \\(W\_{000}=1\\), let \\(M\\) bound the absolute values of its entries and set

\\[ L=8M+1. \\]

In each factor apply

\\[ G=I+L\mathbf1e_0^{\mathsf T}. \\]

This is invertible because \\(\det G=1+L\\).

Every transformed coefficient equals

\\[ L^3+\varepsilon, \qquad |\varepsilon| \le M(3L^2+3L+1)\<L^3. \\]

It is therefore strictly positive.

Use a common \\(M\\) for the transformed \\(U,V\\), so the same local maps make both positive. The rank of \\(V\\) remains one. Apply the same argument separately to the fixed nonzero target.

All changes of basis are fixed independently of \\(n\\) and preserve catalytic convertibility. This proves the positivity clause of Theorem B.

**The encoded computation survives a representation in which every input coefficient is positive. The unrestricted local maps—not the visible signs of the tensor entries—retain the relevant cancellation freedom.**

---

## 5. Consequences beyond numerical stability

### No computable catalyst-dimension bound

There is no computable function of input bit length that bounds the smallest sufficient catalyst dimension on every positive instance.

Otherwise, one could test the finitely many dimensions up to that bound and decide the recursively enumerable–complete set in (2).

This is stronger than merely requiring arbitrarily large catalysts. It rules out **every computable uniform bound**, however rapidly growing, even for the fixed target and fixed source format.

### No complete effective certificates of impossibility

Suppose every impossible conversion had a finite certificate checkable by an algorithm, with all such certificates enumerable.

Positive instances are already recursively enumerable by dimension search. Enumerating the proposed negative certificates in parallel would decide all instances, contradicting (2).

Thus no such sound and complete effective certificate system exists for these exact conversions.

This does not prohibit useful sufficient obstructions. It prohibits their being simultaneously effective and complete.

### The conversion set is not semialgebraic

Fix the tensors \\(U,V,S\\) from Theorem B and consider the real-parameter set

\\[ \mathcal C= \\{x\in\mathbb R:U+xV\succeq\_{\mathrm{cat}}S\\}. \\]

If \\(\mathcal C\\) were semialgebraic, it would be a finite union of intervals and points. Membership of sufficiently large nonnegative integers would then be constant.

But

\\[ \mathcal C\cap\mathbb Z\_{\ge0} \\]

is recursively enumerable–complete, hence not eventually constant. Therefore

\\[ \boxed{\mathcal C\text{ is not semialgebraic}.} \tag{17} \\]

This is a geometric consequence, not merely another description of an algorithmic lower bound: **quantifying over the dimension of an exactly returned auxiliary matrix takes the conversion relation outside finite polynomial-inequality descriptions, even on one fixed affine line.**

---

## 6. A concrete catalyst and falsification checks

The universal construction has a small algebraic test case:

\\[ X^2=I,\qquad Y^2=I,\qquad XY+YX=0. \tag{18} \\]

There is no scalar solution over \\(\mathbb C\\): the first two equations require nonzero \\(x,y\\), while the third requires \\(2xy=0\\).

There is a two-dimensional solution:

\\[ X= \begin{pmatrix} 1&0\\\0&-1 \end{pmatrix}, \qquad Y= \begin{pmatrix} 0&1\\\1&0 \end{pmatrix}. \\]

Here \\(s=3\\), \\(q=7\\), and \\(K=364\\). The compiler gives tensors of formats

\\[ 7\times367\times367, \qquad 7\times365\times365 \\]

satisfying

\\[ \boxed{ T\not\succeq S, \qquad T[2]\succeq S[2]. } \tag{19} \\]

Thus the construction produces genuine catalysis, not merely a formal undecidability reduction.

I checked the full amplified slice identities for this example at \\(d=2\\) and \\(d=4\\) using exact integer arithmetic. The scalar equations have Gröbner basis \\([1]\\). Additional exact checks verified the scalar stabilizer of the marker configuration for \\(q=2,\ldots,7\\), and the integer-enforcing identities for \\(z=\pm1,\ldots,\pm6\\).

verify.py · verification_results.json

These finite checks do not substitute for the general proof. The main adversarial issues are addressed mathematically:

The first map cannot evade the encoded relations by mixing slices, because the rank-drop configuration forces it to be scalar. The other maps cannot use the marker blocks to fake a representation, because the distinguished slice saturates their rank and fixes their output spaces. Complex representations cannot evade the integer encoding, because a simple quotient makes the central parameters scalar integers.

---

## 7. Originality status and limits

There is relevant prior work, and the distinction is important.

Stochastic multipartite catalysis was studied by Chen, Chitambar, Duan, Ji and Winter. The proposed contribution is not the existence of multipartite catalysis in general. [arXiv](https://arxiv.org/abs/1003.3059)

Christandl, Gesmundo, Lysikov and Steffan study partial degeneration and aided rank, including constructions motivated by matrix multiplication and quantum entanglement. Those are closely related operations, but the result proposed here concerns a dimension-preserving encoding into **exact conversion with the same bipartite auxiliary state returned**. [arXiv](https://arxiv.org/abs/2212.14095)

More specifically, Steffan’s 2023 thesis explicitly asks whether an aiding matrix alone can provide an honest catalytic conversion

\\[ T\not\succeq S,\qquad T[d]\succeq S[d]. \\]

The example (19) addresses that precise question. This establishes relevance to a documented research question, **not a claim that it remained unanswered through the present date**. [Copenhagen Math Dept](https://www.math.ku.dk/bibliotek/arkivet/phd-theses/phd23vs.pdf)

I did not locate the dimension-preserving three-party representation compiler or the fixed-positive-affine-family undecidability theorem in the sources checked. The targeted Astra repository searches were also insufficient for a full priority determination.

The proposed new contribution is therefore the **rank-based embedding of arbitrary finite-dimensional algebra representations into unrestricted catalytic tensor restriction**, together with its fixed-format consequences—not the known undecidability of representation existence or the standard Lie-algebra ingredients.

The scope remains exact. The argument does **not** establish a result for approximate conversion, a dimension-independent success-probability guarantee, deterministic catalysis, or catalysts involving all three parties. Nor does it constrain the ordinary matrix-multiplication exponent.

**The mathematical advance proposed in this investigation is a universal encoding mechanism that survives unrestricted cancellation. Its proof is supplied without an outstanding reduction step; its correctness and historical novelty still require independent assessment before it can be classified as a landmark discovery.**